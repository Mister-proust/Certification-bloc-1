import pandas as pd
import requests
import time
import psycopg2
from sqlalchemy import create_engine, text
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DB_CONFIG = {
    "user": USER,  
    "password": PASSWORD, 
    "host": HOST,
    "port": PORT,
    "database": DATABASE
}

def total_pages(api_type: str, annee_min: int = 2013, annee_max: int = 2025):
    base_url = f"https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto/achats/{api_type}"
    params = {
        "type_territoire": "Département",
        "annee_min": annee_min,
        "annee_max": annee_max,
        "size": 1,  
        "page": 1
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json().get("count", 0)
    except Exception as e:
        print(f" Erreur: {e}")
        return None

def get_data(api_type: str, annee_min: int = 2013, annee_max: int = 2025):
    assert api_type in ["produits", "substances"], "Erreur avec l'API"
    base_url = f"https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto/achats/{api_type}"
    params = {
        "type_territoire": "Département",
        "annee_min": annee_min,
        "annee_max": annee_max,
        "size": 20000, 
        "page": 1
    }

    total_lignes = total_pages(api_type, annee_min, annee_max)
    
    all_data = []
    start_time = time.time()
    
    if total_lignes:
        pbar = tqdm(total=total_lignes, desc=f" {api_type.capitalize()}", 
                   unit="lignes", unit_scale=True)
    else:
        pbar = tqdm(desc=f" {api_type.capitalize()}", unit="pages")

    page = 1
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            params["page"] = page
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data_page = response.json().get("data", [])
            
            if not data_page:
                break
                
            all_data.extend(data_page)
            
            if total_lignes:
                pbar.update(len(data_page))
                pbar.set_postfix({
                    'Page': page,
                    'Total': len(all_data),
                    'Vitesse': f"{len(all_data)/(time.time()-start_time):.0f} rec/s"
                })
            else:
                pbar.update(1)
                pbar.set_postfix({
                    'Page': page,
                    'Records': len(all_data)
                })
            
            page += 1
            consecutive_errors = 0
            
        except requests.exceptions.RequestException as e:
            consecutive_errors += 1
            print(f" Erreur à la page {page}: {e}")
            
            if consecutive_errors >= max_consecutive_errors:
                print(f"Trop d'erreurs consécutives, arrêt du processus... ({consecutive_errors}). Arrêt.")
                break
                
            print(f" Pause de {consecutive_errors * 2}s avant de réessayer...")
            time.sleep(consecutive_errors * 2)

    pbar.close()

    duration = time.time() - start_time

    print(f"Récupération terminée de {len(all_data)} lignes en {duration:.2f}s pour {api_type}")
    return pd.DataFrame(all_data)

def clean_produits(df):
    print("Nettoyage des données du dataframe des produits...")
    df = df[["amm", "annee", "code_territoire", "eaj", "quantite", "unite"]]
    df = df[df["code_territoire"] != "0"]
    df = df.rename(columns={
        "code_territoire": "num_département",
        "eaj": "autorise_jardin",
        "quantite": "quantite_en_kg"
    })
    
    colonnes_entiers = ["amm"]
    for col in colonnes_entiers:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    
    df = df.reset_index(drop=True)
    df.insert(0, 'id_produits_vente', df.index)
    print(f"Nettoyage terminé: {len(df)} lignes conservées")

    return df.reset_index(drop=True)

def clean_substances(df):
    print("Nettoyage des données du dataframe des substances chimiques...")
    df = df[df["classification"].isin(["CMR", "T, T+, CMR"])]
    df = df[["amm", "annee", "classification_mention", "code_cas", "code_substance",
             "code_territoire", "fonction", "libelle_substance", "quantite"]]
    df = df[df["code_territoire"] != "0"]
    df = df.rename(columns={
        "code_territoire": "num_département",
        "libelle_substance": "nom_substance",
        "quantite": "quantite_en_kg"
    })
    colonnes_entiers = ["amm", "code_substance"]
    for col in colonnes_entiers:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    
    df = df.reset_index(drop=True)
    df.insert(0, 'id_substance', df.index)
    print(f"Nettoyage terminé: {len(df)} lignes conservées")
    return df.reset_index(drop=True)

def create_schema_if_not_exists(engine, schema):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))

from sqlalchemy import create_engine
import time

def export_to_postgres(df, table_name: str, schema: str):
    print(f"Export des données en cours vers PostgreSQL (table: {schema}.{table_name})...")
    start_time = time.time()
    
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    
    create_schema_if_not_exists(engine, schema)
    
    chunk_size = 10000
    if len(df) > chunk_size:
        for i in range(0, len(df), chunk_size):
            chunk = df[i:i+chunk_size]
            chunk.to_sql(table_name, engine, schema=schema,
                         if_exists="replace" if i == 0 else "append",
                         index=False, method='multi')
    else:
        df.to_sql(table_name, engine, schema=schema, if_exists="replace", index=False)
    
    duration = time.time() - start_time
    print(f"Table '{schema}.{table_name}' exportée en {duration:.2f}s ")

def main():
    total_start_time = time.time()
    schema = "Pollution_Cancer"


    try:
        df_produits = get_data("produits", annee_min=2013, annee_max=2025)
        df_substances = get_data("substances", annee_min=2013, annee_max=2025)

        df_produits_propre = clean_produits(df_produits)
        df_substances_propre = clean_substances(df_substances)

        export_to_postgres(df_produits_propre, "Produits_vente", schema)
        export_to_postgres(df_substances_propre, "Substance_cmr_vente", schema)  # Correction typo

        total_duration = time.time() - total_start_time
        print(f" Récupération des données et stockage en {total_duration/60:.1f} minutes")
        
    except Exception as e:
        print(f"Problème dans le script: {e}")
        raise

if __name__ == "__main__":
    main()
import pandas as pd
import requests
import time
from tqdm import tqdm
from dotenv import load_dotenv
import os
from model.models import ProduitsVente, SubstanceCMRVente
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import text

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path="../.env", override=True)

# Connexion à la base de données PostgreSQL
USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

def total_pages(api_type: str, annee_min: int = 2013, annee_max: int = 2025):
    """
    Récupère le nombre total de lignes disponibles pour une API donnée et une plage d'années.

    Args:
        api_type (str): 'produits' ou 'substances'.
        annee_min (int): Année minimale.
        annee_max (int): Année maximale.

    Returns:
        int: Nombre total de lignes à récupérer.
    """
    url = f"https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto/achats/{api_type}"
    params = {
        "type_territoire": "Département",
        "annee_min": annee_min,
        "annee_max": annee_max,
        "size": 1,
        "page": 1
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json().get("count", 0)
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def get_data(api_type: str, annee_min: int = 2013, annee_max: int = 2025):
    """
    Récupère l'ensemble des données via l'API Hubeau en paginant les résultats.

    Args:
        api_type (str): 'produits' ou 'substances'.
        annee_min (int): Année minimale.
        annee_max (int): Année maximale.

    Returns:
        pd.DataFrame: Données récupérées sous forme de DataFrame.
    """
    assert api_type in ["produits", "substances"], "Erreur avec l'API"
    url = f"https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto/achats/{api_type}"
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
    pbar = tqdm(total=total_lignes, desc=f" {api_type.capitalize()}", unit="lignes")

    page = 1
    while True:
        try:
            params["page"] = page
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json().get("data", [])
            if not data:
                break
            all_data.extend(data)
            pbar.update(len(data))
            pbar.set_postfix(page=page, total=len(all_data))
            page += 1
        except Exception as e:
            print(f"Erreur page {page}: {e}")
            break

    pbar.close()
    print(f"{len(all_data)} lignes récupérées pour {api_type}")
    return pd.DataFrame(all_data)

def retirer_zero(code_str):
    """
    Supprime les zéros non significatifs au début des codes.

    Args:
        code_str (str): Code de département sous forme de chaîne.

    Returns:
        str: Code sans zéros en début de chaîne.
    """
    if isinstance(code_str, str) and code_str.isdigit():
        return str(int(code_str))
    return code_str

def clean_produits(df):
    """
    Nettoie et prépare les données des produits avant insertion en base.

    Args:
        df (pd.DataFrame): Données brutes des produits.

    Returns:
        pd.DataFrame: Données nettoyées et structurées.
    """
    print("Nettoyage des produits...")
    df = df[["amm", "annee", "code_territoire", "eaj", "quantite", "unite"]]
    df["code_territoire"] = df["code_territoire"].astype(str)
    df = df[df["code_territoire"] != "00"]
    df = df.rename(columns={
        "code_territoire": "num_departement",
        "eaj": "autorise_jardin",
        "quantite": "quantite_en_kg"
    })
    df["num_departement"] = df["num_departement"].apply(retirer_zero)
    df["amm"] = pd.to_numeric(df["amm"], errors="coerce").astype("Int64")
    df = df.reset_index(drop=True)
    df.insert(0, "id_produits_vente", df.index)
    return df

def clean_substances(df):
    """
    Nettoie et prépare les données des substances CMR avant insertion en base.

    Args:
        df (pd.DataFrame): Données brutes des substances.

    Returns:
        pd.DataFrame: Données nettoyées et structurées.
    """
    print("Nettoyage des substances CMR...")
    df = df[df["classification"].isin(["CMR", "T, T+, CMR"])]
    df = df[["amm", "annee", "classification_mention", "code_cas", "code_substance",
             "code_territoire", "fonction", "libelle_substance", "quantite"]]
    df["code_territoire"] = df["code_territoire"].astype(str)
    df = df[df["code_territoire"] != "00"]
    df = df.rename(columns={
        "code_territoire": "num_departement",
        "libelle_substance": "nom_substance",
        "quantite": "quantite_en_kg"
    })
    df["num_departement"] = df["num_departement"].apply(retirer_zero)
    df["amm"] = pd.to_numeric(df["amm"], errors="coerce").astype("Int64")
    df["code_substance"] = pd.to_numeric(df["code_substance"], errors="coerce").astype("Int64")
    df = df.reset_index(drop=True)
    df.insert(0, "id_substance", df.index)
    return df

def insert_sqlmodel_objects(df: pd.DataFrame, model_class, session: Session, batch_size=5000):
    """
    Insère les données nettoyées dans la base PostgreSQL par lot.

    Args:
        df (pd.DataFrame): Données à insérer.
        model_class: Modèle SQLModel correspondant.
        session (Session): Session active de base de données.
        batch_size (int): Nombre de lignes insérées par transaction.
    """
    records = df.to_dict(orient="records")
    objects = [model_class(**row) for row in records]
    for i in range(0, len(objects), batch_size):
        session.add_all(objects[i:i+batch_size])
        session.commit()

def get_existing_amm(engine) -> set:
    """
    Récupère la liste des AMM déjà existants dans la table 'amm_produits'.

    Args:
        engine: Connexion SQLAlchemy à la base.

    Returns:
        set: Ensemble des AMM existants.
    """
    with Session(engine) as session:
        result = session.exec(text('SELECT amm FROM "Pollution_Cancer".amm_produits')).all()
        return [row[0] for row in result]
    
def run():
    """
    Exécute l'ensemble du processus :
    - Récupération des données via API
    - Nettoyage des données
    - Filtrage selon les AMM existants
    - Insertion dans la base de données
    """
    SQLModel.metadata.create_all(engine)

    try:
        # Récupération des données produits et substances
        df_produits = get_data("produits")
        df_substances = get_data("substances")

        # Nettoyage des données
        df_produits_clean = clean_produits(df_produits)
        df_substances_clean = clean_substances(df_substances)

        # Filtrage sur les AMM existants
        print("Récupération des AMM existants dans la table amm_produits...")
        amm_existants = get_existing_amm(engine)

        print(f"Filtrage des produits sur {len(df_produits_clean)} lignes...")
        df_produits_clean = df_produits_clean[df_produits_clean["amm"].isin(amm_existants)]
        print(f"{len(df_produits_clean)} produits conservés après filtrage.")

        print(f"Filtrage des substances sur {len(df_substances_clean)} lignes...")
        df_substances_clean = df_substances_clean[df_substances_clean["amm"].isin(amm_existants)]
        print(f"{len(df_substances_clean)} substances conservées après filtrage.")

        # Insertion en base
        with Session(engine) as session:
            insert_sqlmodel_objects(df_produits_clean, ProduitsVente, session)
            insert_sqlmodel_objects(df_substances_clean, SubstanceCMRVente, session)

        print("Données achat substances et produits chimiques insérées avec succès.")

    except Exception as e: 
        print(f"Problème dans le script : {e}")
        raise

if __name__ == "__main__":
    run()

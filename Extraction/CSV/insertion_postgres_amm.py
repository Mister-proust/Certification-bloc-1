import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

user = USER
password = PASSWORD
host = HOST
port = PORT
database = DATABASE
schema = "Pollution_Cancer"
table = "amm_mention_danger"
table2 = "amm_produits"


df_amm_danger = pd.read_csv("../../data/produits_classe_et_mention_danger_utf8.csv", sep=";")

df_amm_danger = df_amm_danger.drop(columns=["Unnamed: 4"])

df_amm_danger= df_amm_danger.rename(columns={
    "numero AMM": "amm",
    "nom produit" : "Nom_produit",
    "Libellé court": "Libellé_court",
    "Libelle long": "Toxicite_produit"
      })

df_produits = pd.read_csv("../../data/produits_utf8.csv", sep=";")

df_produits = df_produits.drop(columns=["type produit"])
df_produits = df_produits.drop(columns=["Unnamed: 18"])

df_produits= df_produits.rename(columns={
    "numero AMM": "amm",
    "nom produit" : "Nom_produit",
    "seconds noms commerciaux" : "Second_noms_commerciaux",
    "type commercial" : "Type_commercial",
    "gamme usage" : "Gamme_usage",
    "mentions autorisees" : "Mentions_autorisees",
    "restrictions usage" : "Restrictions_usage", 
    "restrictions usage libelle" : "Restrictions_usage_libelle",
    "Substances actives" : "Substances_actives",
    "fonctions" : "Fonctions",
    "formulations" : "Formulations",
    "Etat d'autorisation" : "Etat_d_autorisation",
    "Date de retrait du produit" : "Date_de_retrait",
    "Date de première autorisation" : "Date_première_autorisation",
    "Numéro AMM du produit de référence" : "Numero_AMM_reference",
    "Nom du produit de référence" : "Nom_produit_reference"
      })

df_amm_danger = df_amm_danger.reset_index(drop=False)
df_amm_danger = df_amm_danger.rename(columns={"index":"id_amm_danger"})
cols = df_amm_danger.columns.tolist()
cols = ['id_amm_danger'] + [col for col in cols if col != 'id_amm_danger']
df_amm_danger = df_amm_danger[cols]

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

with engine.connect() as conn:
    conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}";'))
    conn.execute(text(f'SET search_path TO {schema};'))
    
    df_amm_danger.to_sql(
        table,
        con=conn,
        schema=schema,
        index=False,
        if_exists='replace',  
        method='multi'
    )

    df_produits.to_sql(
        table2,
        con=conn,
        schema=schema,
        index=False,
        if_exists='replace',  
        method='multi'
    )
    conn.commit()

print(f"Données insérées avec succès, veuillez vérifier.")

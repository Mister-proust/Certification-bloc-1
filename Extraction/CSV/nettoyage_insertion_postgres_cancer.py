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
table = "Effectif_cancer"

df = pd.read_csv("../../data/effectifs.csv", sep=";")

df = df[["annee", "patho_niv1", "patho_niv2", "patho_niv3", "cla_age_5", "sexe", "dept", "Ntop", "Npop"]]

df_cancer = df[df["patho_niv1"] == "Cancers"]

df_final = df_cancer[
    df_cancer["patho_niv2"].notna() &
    df_cancer["patho_niv3"].notna()
]

df_final = df_final.rename(columns={
    "annee": "Annee",
    "patho_niv1": "Pathologie",
    "patho_niv2": "Type_cancer",
    "patho_niv3": "Suivi_patho",
    "cla_age_5": "Classe_age",
    "sexe": "Sexe",
    "dept": "Departement",
    "Ntop": "Effectif_patients",
    "Npop": "Effectif_total"
})

df_final["Effectif_patients"] = pd.to_numeric(df_final["Effectif_patients"], errors='coerce')
df_final["Effectif_total"] = pd.to_numeric(df_final["Effectif_total"], errors='coerce')

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

with engine.connect() as conn:
    conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}";'))
    conn.execute(text(f'SET search_path TO {schema};'))
    
    df_final.to_sql(
        table,
        con=conn,
        schema=schema,
        index=False,
        if_exists='replace',  
        method='multi'
    )

    conn.commit()

print(f"Données insérées avec succès dans {schema}.{table}")

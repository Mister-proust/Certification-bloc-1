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
table = "Effectif_departement"
table2 = "Metada_effectif_departement"


df = pd.read_csv("../../data/eff_pop.csv", sep=";")

df_metadata = pd.read_csv("../../data/metadata_eff_pop.csv", sep=";")

df = df[df["GEO_OBJECT"] == "DEP"]

df_metadata["index"] = df_metadata.index

df_metadata = df_metadata[~((df_metadata["COD_VAR"] == "GEO") & (df_metadata["index"] > 174))]

df_metadata = df_metadata.drop(columns=["index"])

df_metadata.loc[(df_metadata["COD_VAR"] == "AGE") & (df_metadata["COD_MOD"] == "_T"),"COD_MOD"] = "_Ta"

df_metadata.loc[(df_metadata["COD_VAR"] == "GEO") & (df_metadata["COD_MOD"] == "F"),"COD_MOD"] = "Fr"

df.loc[(df["AGE"] == "_T"),"AGE"] = "_Ta"

df.loc[(df["GEO"] == "F"),"GEO"] = "Fr"

df= df.rename(columns={
    "GEO": "Num_dep",
    "SEX" : "Sexe",
    "GEO_OBJECT": "Carac_dep",
    "AGE": "Age",
    "EP_MEASURE": "Carac_mesure",
    "OBS_STATUS_FR": "Chiffre_def",
    "TIME_PERIOD": "Annee",
    "OBS_VALUE": "Effectif" })

df = df.reset_index(drop=False)
df = df.rename(columns={"index":"id_effectif_departement"})
cols = df.columns.tolist()
cols = ['id_effectif_departement'] + [col for col in cols if col != 'id_effectif_departement']
df = df[cols]



engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

with engine.connect() as conn:
    conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}";'))
    conn.execute(text(f'SET search_path TO {schema};'))
    
    df.to_sql(
        table,
        con=conn,
        schema=schema,
        index=False,
        if_exists='replace',  
        method='multi'
    )

    df_metadata.to_sql(
        table2,
        con=conn,
        schema=schema,
        index=False,
        if_exists='replace',  
        method='multi'
    )
    conn.commit()

print(f"Données insérées avec succès, veuillez vérifier.")

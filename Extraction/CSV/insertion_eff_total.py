import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.db_init import engine
from model.models import  EffectifDepartement
from sqlmodel import Session

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

df = pd.read_csv("../data/eff_pop.csv", sep=";")

df = df[df["GEO_OBJECT"] == "DEP"]

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

def retirer_zero(code_str):
    if isinstance(code_str, str) and code_str.isdigit():
        return str(int(code_str)) 
    return code_str

df["Num_dep"] = df["Num_dep"].apply(retirer_zero)


engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

liste_Effectif = [
    EffectifDepartement(**row) for row in df.to_dict(orient="records")
]


with Session(engine) as session:
    session.add_all(liste_Effectif)
    session.commit()

print(f"Données insérées avec succès, veuillez vérifier.")

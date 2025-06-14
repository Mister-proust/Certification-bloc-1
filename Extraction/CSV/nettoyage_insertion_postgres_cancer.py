import pandas as pd
from sqlalchemy import text
from dotenv import load_dotenv
import os
from model.models import EffectifCancer
from sqlmodel import Session, create_engine

load_dotenv(dotenv_path="../.env", override=True)

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

df = pd.read_csv("../data/effectifs.csv", sep=";")

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

df_final = df_final.reset_index(drop=True)
df_final.insert(0, 'id_effectif_cancer', df_final.index)

df_final["Sexe"] = df_final["Sexe"].replace({1: "M", 2: "F", 9: "_T"})
df_final["Classe_age"] = df_final["Classe_age"].replace({"00-04": "Y_LT5", "05-09": "Y5T9", "10-14": "Y10T14", "15-19": "Y15T19", "20-24": "Y20T24", "25-29": "Y25T29", "30-34": "Y30T34", "95et+": "Y_GE95", "35-39": "Y35T39", "40-44": "Y40T44", "45-49": "Y45T49", "90-94": "Y90T94", "50-54": "Y50T54", "55-59": "Y55T59", "85-89": "Y85T89", "60-64": "Y60T64", "80-84": "Y80T84", "75-79": "Y75T79", "65-69": "Y65T69", "70-74": "Y70T74", "tsage": "_T" })

def retirer_zero(code_str):
    if isinstance(code_str, str) and code_str.isdigit():
        return str(int(code_str)) 
    return code_str

df_final["Departement"] = df_final["Departement"].apply(retirer_zero)


engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

liste_effectif_cancer = [
    EffectifCancer(**row) for row in df_final.to_dict(orient="records")
]

with Session(engine) as session:
    session.add_all(liste_effectif_cancer)
    session.commit()

print(f"Données insérées avec succès dans {schema}.{table}")

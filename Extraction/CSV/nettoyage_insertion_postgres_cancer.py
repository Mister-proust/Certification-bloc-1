import pandas as pd
from sqlalchemy import text
from dotenv import load_dotenv
import os
from model.models import EffectifCancer
from sqlmodel import Session, create_engine

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path="../.env", override=True)

# Paramètres de connexion à la base de données PostgreSQL
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


def run(): 
    """
    Fonction principale qui :
    - Charge et filtre les données sur les effectifs de patients atteints de cancer.
    - Nettoie, restructure et formate les données.
    - Insère les données dans la base PostgreSQL.
    """

    # Chargement des données brutes depuis le fichier CSV
    df = pd.read_csv("../data/effectifs.csv", sep=";")

    # Sélection des colonnes d'intérêt
    df = df[["annee", "patho_niv1", "patho_niv2", "patho_niv3", "cla_age_5", "sexe", "dept", "Ntop", "Npop"]]

    # Filtrage des lignes correspondant aux cancers uniquement
    df_cancer = df[df["patho_niv1"] == "Cancers"]

    # Suppression des lignes incomplètes (sans typage précis de cancer)
    df_final = df_cancer[
        df_cancer["patho_niv2"].notna() &
        df_cancer["patho_niv3"].notna()
    ]

    # Renommage des colonnes pour plus de clarté
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

    # Conversion des effectifs en valeurs numériques
    df_final["Effectif_patients"] = pd.to_numeric(df_final["Effectif_patients"], errors='coerce')
    df_final["Effectif_total"] = pd.to_numeric(df_final["Effectif_total"], errors='coerce')

    # Réinitialisation des index et ajout d'un identifiant unique
    df_final = df_final.reset_index(drop=True)
    df_final.insert(0, 'id_effectif_cancer', df_final.index)

    # Remplacement des codes de sexe par des libellés explicites
    df_final["Sexe"] = df_final["Sexe"].replace({1: "M", 2: "F", 9: "_T"})

    # Harmonisation des classes d'âge avec des libellés courts
    df_final["Classe_age"] = df_final["Classe_age"].replace({"00-04": "Y_LT5", "05-09": "Y5T9", "10-14": "Y10T14", "15-19": "Y15T19", "20-24": "Y20T24", "25-29": "Y25T29", "30-34": "Y30T34", "95et+": "Y_GE95", "35-39": "Y35T39", "40-44": "Y40T44", "45-49": "Y45T49", "90-94": "Y90T94", "50-54": "Y50T54", "55-59": "Y55T59", "85-89": "Y85T89", "60-64": "Y60T64", "80-84": "Y80T84", "75-79": "Y75T79", "65-69": "Y65T69", "70-74": "Y70T74", "tsage": "_T" })

    def retirer_zero(code_str):
        """
        Supprime les zéros non significatifs au début des codes de département.

        Args:
            code_str (str): Code de département sous forme de chaîne.

        Returns:
            str: Code sans zéros initiaux.
        """
        if isinstance(code_str, str) and code_str.isdigit():
            return str(int(code_str)) 
        return code_str

    # Nettoyage des numéros de département
    df_final["Departement"] = df_final["Departement"].apply(retirer_zero)

    # Connexion à la base de données PostgreSQL
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

    # Conversion des lignes en objets SQLModel
    liste_effectif_cancer = [
        EffectifCancer(**row) for row in df_final.to_dict(orient="records")
    ]

    # Insertion des données dans la base PostgreSQL
    with Session(engine) as session:
        session.add_all(liste_effectif_cancer)
        session.commit()

    print(f"Données sur le cancer insérées avec succès dans {schema}.{table}")

if __name__ == "__main__":
    run()

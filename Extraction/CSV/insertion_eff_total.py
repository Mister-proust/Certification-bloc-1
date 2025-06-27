import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.db_init import engine
from model.models import  EffectifDepartement
from sqlmodel import Session

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path="../.env", override=True)

# Connexion à la base de données PostgreSQL
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

def run():
    """
    Fonction principale qui :
    - Charge les données démographiques depuis un fichier CSV
    - Nettoie et restructure les données
    - Insère les effectifs départementaux dans la base PostgreSQL
    """

    # Chargement des données depuis le fichier CSV
    df = pd.read_csv("../data/eff_pop.csv", sep=";")

    # Filtrage des lignes concernant les départements uniquement
    df = df[df["GEO_OBJECT"] == "DEP"]

    # Renommage des colonnes pour une meilleure lisibilité
    df= df.rename(columns={
        "GEO": "Num_dep",
        "SEX" : "Sexe",
        "GEO_OBJECT": "Carac_dep",
        "AGE": "Age",
        "EP_MEASURE": "Carac_mesure",
        "OBS_STATUS_FR": "Chiffre_def",
        "TIME_PERIOD": "Annee",
        "OBS_VALUE": "Effectif" })

    # Réinitialisation des index et création d'une clé primaire id_effectif_departement
    df = df.reset_index(drop=False)
    df = df.rename(columns={"index":"id_effectif_departement"})

    # Réorganisation des colonnes pour mettre l'ID en première position
    cols = df.columns.tolist()
    cols = ['id_effectif_departement'] + [col for col in cols if col != 'id_effectif_departement']
    df = df[cols]

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
    df["Num_dep"] = df["Num_dep"].apply(retirer_zero)

    # Connexion à la base de données
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

    # Conversion des lignes en objets SQLModel
    liste_Effectif = [
        EffectifDepartement(**row) for row in df.to_dict(orient="records")
    ]

    # Insertion en base via une session SQLModel
    with Session(engine) as session:
        session.add_all(liste_Effectif)
        session.commit()

    print(f"Données sur les effectifs totaux insérées avec succès, veuillez vérifier.")

if __name__ == "__main__":
    run()

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.models import  MetadataAge 
from sqlmodel import Session

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path="../.env", override=True)

# Paramètres de connexion à la base de données PostgreSQL
USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)
 
def run(): 
    """
    Fonction principale qui :
    - Insère des métadonnées d'âges dans la table MetadataAge.
    - Ces métadonnées permettent de regrouper les classes d'âge et de leur associer un âge médian.
    """

    with Session(engine) as session: 
        # Sélection du schéma dans PostgreSQL
        session.exec(text(f'SET search_path TO "Pollution_Cancer";'))

        # Données à insérer : codes d'âge, libellés et âges médians associés
        data_to_insert= [
            {"Code": "Y_LT20", "Libelle": "0 à 19 ans", "Age_median": "10"},
            {"Code": "Y20T39", "Libelle": "De 20 à 39 ans","Age_median": "30"},
            {"Code": "Y40T59", "Libelle": "De 40 à 59 ans", "Age_median" : "50"},
            {"Code": "Y60T74", "Libelle": "De 60 à 74 ans", "Age_median" : "67"},
            {"Code": "Y_GE75", "Libelle": "75 ans ou plus", "Age_median" : "85"},
            {"Code": "Y60T64", "Libelle": "De 60 à 64 ans", "Age_median" : "62"},
            {"Code": "Y65T69", "Libelle": "De 65 à 69 ans", "Age_median" : "67"},
            {"Code": "Y70T74", "Libelle": "De 70 à 74 ans", "Age_median" : "72"},
            {"Code": "Y75T79", "Libelle": "De 75 à 79 ans", "Age_median" : "77"},
            {"Code": "Y80T84", "Libelle": "De 80 à 84 ans", "Age_median" : "82"},
            {"Code": "Y85T89", "Libelle": "De 85 à 89 ans", "Age_median" : "87"},
            {"Code": "Y90T94", "Libelle": "De 90 à 94 ans", "Age_median" : "92"},
            {"Code": "Y_GE95", "Libelle": "95 ans ou plus", "Age_median" : "97"},
            {"Code": "Y_LT5", "Libelle": "Moins de 5 ans", "Age_median" : "2"},
            {"Code": "Y5T9", "Libelle": "De 5 à 9 ans", "Age_median" : "7"},
            {"Code": "Y10T14", "Libelle": "De 10 à 14 ans", "Age_median" : "12"},
            {"Code": "Y15T19", "Libelle": "De 15 à 19 ans", "Age_median" : "17"},
            {"Code": "Y20T24", "Libelle": "De 20 à 24 ans", "Age_median" : "22"},
            {"Code": "Y25T29", "Libelle": "De 25 à 29 ans", "Age_median" : "27"},
            {"Code": "Y30T34", "Libelle": "De 30 à 34 ans", "Age_median" : "32"},
            {"Code": "Y35T39", "Libelle": "De 35 à 39 ans", "Age_median" : "37"},
            {"Code": "Y40T44", "Libelle": "De 40 à 44 ans", "Age_median" : "42"},
            {"Code": "Y45T49", "Libelle": "De 45 à 49 ans", "Age_median" : "47"},
            {"Code": "Y50T54", "Libelle": "De 50 à 54 ans", "Age_median" : "52"},
            {"Code": "Y55T59", "Libelle": "De 55 à 59 ans", "Age_median" : "57"},
            {"Code": "_Z", "Libelle": "Non applicable", "Age_median" : None},
            {"Code": "_T", "Libelle": "Total", "Age_median" : None}
        ]
        
        # Création et insertion des objets MetadataAge
        for item_data in data_to_insert:
            metadata_age = MetadataAge(**item_data)
            session.add(metadata_age)
        
        # Validation de l'insertion
        session.commit()

        print("metadata_age inséré avec succès")



if __name__ == "__main__":
    run()


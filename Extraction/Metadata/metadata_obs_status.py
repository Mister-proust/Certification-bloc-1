from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.models import  MetadataObsStatus
from sqlmodel import Session

# Chargement des variables d'environnement
load_dotenv(dotenv_path="../.env", override=True)

# Paramètres de connexion PostgreSQL
USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

# Construction de l'URL de connexion
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

def run():
    """
    Insère dans la table MetadataObsStatus les statuts d'observation :
    - Définitif
    - Provisoire
    Ces statuts permettent de qualifier le niveau de fiabilité des effectifs.
    """
    with Session(engine) as session: 
        # Sélection du schéma PostgreSQL ciblé
        session.exec(text(f'SET search_path TO "Pollution_Cancer";'))

        # Données à insérer
        data_to_insert= [
            {"Code": "D", "Libelle": "Définitif"},
            {"Code": "PROV", "Libelle": "Provisoire"}
        ]

        # Insertion des données
        for item_data in data_to_insert:
            metadata_obs_status = MetadataObsStatus(**item_data)
            session.add(metadata_obs_status)
        
        # Validation des insertions
        session.commit()
    print("metadata_obs_status inséré avec succès")

if __name__ == "__main__":
    run()

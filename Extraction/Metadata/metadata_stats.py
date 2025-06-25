from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.models import  MetadataStats 
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
    Insère dans la table MetadataStats les libellés statistique :
    Ces statuts permettent de qualifier les codes utilisées dans les statistiques
    des effectifs.
    """
    with Session(engine) as session: 
        # Sélection du schéma PostgreSQL ciblé
        session.exec(text(f'SET search_path TO "Pollution_Cancer";'))

        # Données à insérer
        data_to_insert= [
            {"Code": "POP", "Libelle": "Population"},
            {"Code": "PT_YGE65_IN_Y20T64", "Libelle": "Proportion des personnes de plus de 65 ans par rapport aux personnes de 20 à 64 ans"},
            {"Code": "AVERAGE", "Libelle": "Age moyen"},
            {"Code": "MEDAGE", "Libelle": "Age médian"}
        ]

        # Insertion des données
        for item_data in data_to_insert:
            metadata_stats = MetadataStats(**item_data)
            session.add(metadata_stats)
        
        # Validation des insertions
        session.commit()
        print("metadata_stats inséré avec succès")


if __name__ == "__main__":
    run()


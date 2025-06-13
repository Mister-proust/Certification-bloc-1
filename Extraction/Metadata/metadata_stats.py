from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.models import  MetadataStats 
from sqlmodel import Session

load_dotenv(dotenv_path="../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

# Ajout des lignes dans la table.
def run(): 
    with Session(engine) as session: 
        session.exec(text(f'SET search_path TO "Pollution_Cancer";'))
        data_to_insert= [
            {"Code": "POP", "Libelle": "Population"},
            {"Code": "PT_YGE65_IN_Y20T64", "Libelle": "Proportion des personnes de plus de 65 ans par rapport aux personnes de 20 à 64 ans"},
            {"Code": "AVERAGE", "Libelle": "Age moyen"},
            {"Code": "MEDAGE", "Libelle": "Age médian"}
        ]
        for item_data in data_to_insert:
            metadata_stats = MetadataStats(**item_data)
            session.add(metadata_stats)
        
        session.commit()
        print("metadata_stats inséré avec succès")


if __name__ == "__main__":
    run()


from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from model.models import  MetadataObsStatus
from sqlmodel import Session

load_dotenv(dotenv_path="../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

#Ajout des lignes dans la table
def run():
    with Session(engine) as session: 
        session.exec(text(f'SET search_path TO "Pollution_Cancer";'))
        data_to_insert= [
            {"Code": "D", "Libelle": "Définitif"},
            {"Code": "PROV", "Libelle": "Provisoire"}
        ]
        for item_data in data_to_insert:
            metadata_obs_status = MetadataObsStatus(**item_data)
            session.add(metadata_obs_status)
        
        session.commit()
    print("metadata_obs_status inséré avec succès")

if __name__ == "__main__":
    run()

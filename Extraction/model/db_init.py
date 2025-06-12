import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel

from model.models import EffectifCancer, Effectifdepartement, Metadataeffectifdepartement, Produitsvente, Substancecmrvente, Ammmentiondanger, Ammproduits


load_dotenv(dotenv_path="../../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

schema = "Pollution_Cancer" 

def create_db_and_tables():
    print(f"Tentative de connexion à la base de données : {DATABASE}")
    try:
        with engine.connect() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}";'))
            conn.execute(text(f'SET search_path TO {schema};'))
            conn.commit() 
            SQLModel.metadata.create_all(conn)
            conn.commit()
            print("Tables créées avec succès veuillez vérifier.")

    except Exception as e:
        print(f"Erreur lors de la création de la base de données et des tables: {e}")

if __name__ == "__main__":
    create_db_and_tables()
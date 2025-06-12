from sqlalchemy import create_engine, MetaData, Table, Column, String
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

metadata = MetaData(schema="Pollution_Cancer")

metadata_obs_status = Table(
    "metadata_obs_status", metadata,
    Column("Code", String, primary_key=True),
    Column("Libelle", String)
)

metadata.create_all(engine, checkfirst=True)

#Ajout des lignes dans la table
def run():
    with engine.begin() as conn: 
        conn.execute(metadata_obs_status.insert().values([
            {"Code": "D", "Libelle": "Définitif"},
            {"Code": "PROV", "Libelle": "Provisoire"}
        ]))
        conn.commit()
    print("metadata_obs_status inséré avec succès")

if __name__ == "__main__":
    run()

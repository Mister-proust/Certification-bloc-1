import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel

# Importation des modèles de tables à créer
from model.models import EffectifCancer, EffectifDepartement, ProduitsVente, SubstanceCMRVente, AmmMentionDanger, AmmProduits, MetadataAge, MetadataSexe, MetadataDepartement, MetadataAnnee, MetadataObsStatus, MetadataStats


# Chargement des variables d'environnement
load_dotenv(dotenv_path="../.env", override=True)

# Paramètres de connexion à la base de données PostgreSQL
USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

# Construction de l'URL de connexion
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

# Nom du schéma PostgreSQL
schema = "Pollution_Cancer" 

def create_db_and_tables():
    """
    Crée le schéma et les tables nécessaires dans la base de données PostgreSQL.

    Étapes :
    1. Connexion à la base de données.
    2. Création du schéma s'il n'existe pas.
    3. Application du schéma (search_path).
    4. Création des tables à partir des modèles importés.
    """
    print(f"Tentative de connexion à la base de données : {DATABASE}")
    try:
        with engine.connect() as conn:
            # Création du schéma s'il n'existe pas
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}";'))

            # Application du schéma pour la session
            conn.execute(text(f'SET search_path TO {schema};'))

            # Validation des commandes précédentes
            conn.commit() 

            # Création des tables définies dans les modèles
            SQLModel.metadata.create_all(conn)

            # Validation de la création des tables
            conn.commit()
            print("Tables créées avec succès veuillez vérifier.")

    except Exception as e:
        print(f"Erreur lors de la création de la base de données et des tables: {e}")

if __name__ == "__main__":
    create_db_and_tables()
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connection_postgres():
    """
    Établit une connexion à la base de données PostgreSQL en utilisant
    les variables d'environnement définies dans le fichier .env.

    Variables d'environnement utilisées :
        - HOST_POSTGRES : adresse du serveur PostgreSQL
        - DATABASE_POSTGRES : nom de la base de données
        - USER_POSTGRES : nom d'utilisateur pour la connexion
        - PASSWORD_POSTGRES : mot de passe associé à l'utilisateur
        - PORT_POSTGRES : port du serveur PostgreSQL (ex: 5432)

    Returns:
        psycopg2.extensions.connection : objet de connexion PostgreSQL.

    Note:
        La fonction charge automatiquement les variables d'environnement au démarrage
        grâce à la librairie `dotenv`. Assurez-vous que le fichier `.env` est bien présent
        et correctement configuré dans le répertoire racine du projet.
    """
    return psycopg2.connect(
        host=os.getenv("HOST_POSTGRES"),
        dbname=os.getenv("DATABASE_POSTGRES"),
        user=os.getenv("USER_POSTGRES"),
        password=os.getenv("PASSWORD_POSTGRES"),
        port=os.getenv("PORT_POSTGRES")
    )

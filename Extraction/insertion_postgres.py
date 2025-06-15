from Metadata.metadata_obs_status import run as run_obs_status
from Metadata.metadata_stats import run as run_stats
from Metadata.metadata_sexe import run as run_sexe
from Metadata.metadata_departement import run as run_departement
from Metadata.metadata_annee import run as run_annee
from Metadata.metadata_age import run as run_age
from CSV.insertion_postgres_amm import run as run_amm
from CSV.nettoyage_insertion_postgres_cancer import run as run_cancer
from CSV.insertion_eff_total import run as run_eff_total
from API.Extraction_stockage_achat import run as run_api_achat
from model.db_init import create_db_and_tables
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

if __name__ == "__main__":

   print("Insertion des tables avec contraintes dans la base de données ...")
   create_db_and_tables()

   print("Insertion des métadatas en cours ...")
   run_obs_status()
   run_stats()
   run_sexe()
   run_departement()
   run_annee()
   run_age()

   print ("Insertion des métadatas terminée, insertion des données amm, effectif et cancer en cours...")
   run_amm()
   run_cancer()
   run_eff_total()
   run_api_achat()

   print("insertion des données terminée, veuillez vérifier.")


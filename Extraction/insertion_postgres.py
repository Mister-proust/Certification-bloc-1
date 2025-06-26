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
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

def setup_logging():
    """
    Configure le système de logs. 
    Crée un fichier de logs horodaté et configure l'affichage des logs dans le terminal.

    Retourne:
        logger: Instance du logger configuré.
    """
    os.makedirs("logs", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/db_insertion_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("="*80)
    logger.info(f"Début de l'insertion en base de données - {datetime.now()}")
    logger.info(f"Fichier de logs : {log_filename}")
    logger.info("="*80)
    
    return logger

def execute_step(step_name, step_function, logger):
    """
    Exécute une étape de traitement et mesure son temps d'exécution.

    Args:
        step_name (str): Nom de l'étape en cours.
        step_function (function): Fonction à exécuter.
        logger: Logger pour afficher les informations et erreurs.

    Retourne:
        tuple: (bool succès, résultat ou None)
    """
    logger.info(f"Début de l'insertion de - {step_name}")
    start_time = time.time()
    
    try:
        result = step_function()
      
        execution_time = time.time() - start_time
        logger.info(f"Insertion réussie ! - {step_name} - Temps: {execution_time:.2f}s")
        
        return True, result
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Problème lors de l'insertion- {step_name} - Temps: {execution_time:.2f}s")
        logger.error(f"Voici l'erreur détaillée: {str(e)}")
        logger.exception("Trace complète:")
        
        return False, None
    
def log_database_info(logger):
    """
    Affiche les informations de connexion à la base de données dans les logs.

    Args:
        logger: Logger pour afficher les informations.
    """
    try:
        load_dotenv()
        db_host = os.getenv('DB_HOST', 'localhost')
        db_name = os.getenv('DB_NAME', 'non_défini')
        db_user = os.getenv('DB_USER', 'non_défini')
        
        logger.info(f"Configuration BDD - Host: {db_host}, DB: {db_name}, User: {db_user}")
        
    except Exception as e:
        logger.warning(f"Impossible de récupérer les infos sur la base de données: {e}")


def main():
   """
    Fonction principale qui orchestre :
    - La création des tables en base de données.
    - L'insertion des métadonnées.
    - L'insertion des données CSV et API.
    - La gestion des logs et du suivi d'exécution.
    """
   logger = setup_logging()
   total_start_time = time.time()
   steps_success = 0
   steps_total = 0
   failed_steps = []

   try : 
       log_database_info(logger)

       logger.info(f"Création des tables de données en cours...")
       success, _ = execute_step("Tables vides avec contraintes en cours de création...", create_db_and_tables, logger)
       steps_total += 1
       if success:
            steps_success += 1
       else:
         failed_steps.append("Création des tables")
         logger.critical("Arrêt du processus - Impossible de créer les tables")
         return

       logger.info("Insertion des métadatas en cours ...")
       metadata_insertion = [
         run_obs_status(),
         run_stats(),
         run_sexe(),
         run_departement(),
         run_annee(),
         run_age(),]
       for step_name, step_function in metadata_insertion:
            success, _ = execute_step(step_name, step_function, logger)
            steps_total += 1
            if success:
                steps_success += 1
            else:
                failed_steps.append(step_name)

       logger.info("Insertion des métadatas terminée, insertion des données amm, effectif et cancer en cours...")
       data_insertion = [
      run_amm(),
      run_cancer(),
      run_eff_total(),
      run_api_achat(),]

       for step_name, step_function in data_insertion:
               success, _ = execute_step(step_name, step_function, logger)
               steps_total += 1
               if success:
                  steps_success += 1
               else:
                  failed_steps.append(step_name)
         
   except Exception as e:
         logger.critical(f"Erreur critique dans le processus principal: {e}")
         logger.exception("Stack trace:")

   finally:
        total_time = time.time() - total_start_time
        success_rate = (steps_success / steps_total * 100) if steps_total > 0 else 0
        
        logger.info("="*80)
        logger.info(f"Temps total d'exécution: {total_time:.2f} secondes")
        logger.info(f"Étapes réussies: {steps_success}/{steps_total} ({success_rate:.1f}%)")
        
        if failed_steps:
            logger.error(f"Étapes échouées: {', '.join(failed_steps)}")
            logger.warning("Attention, insertion incomplète ! - Vérifiez les erreurs ci-dessus")
        else:
            logger.info("Insertion en base de données terminée avec succès.")
        
        logger.info(f"Fin de l'insertion en base de données. - {datetime.now()}")
        logger.info("="*80)
        
        if failed_steps:
            print(f"Insertion terminée avec {len(failed_steps)} erreur(s), consultez les logs pour plus de détails.")
        else:
            print("Insertion terminée avec succès!, consultez les logs pour le détail complet.")


if __name__ == "__main__":
    main()


from Metadata.metadata_obs_status import run as run_obs_status
from Metadata.metadata_stats import run as run_stats
from Metadata.metadata_sexe import run as run_sexe
from Metadata.metadata_departement import run as run_departement
from Metadata.metadata_annee import run as run_annee
from Metadata.metadata_age import run as run_age

if __name__ == "__main__":
   run_obs_status()
   run_stats()
   run_sexe()
   run_departement()
   run_annee()
   run_age()

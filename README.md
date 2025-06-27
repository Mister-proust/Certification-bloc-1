## Certification-bloc-1

Ce projet a pour objectif en mettant en corrélation des jeux de data autour de
l’incidence du cancer et de l’achat de substances chimiques considérées comme
cancérigènes, d’observer s’il pourrait y avoir un rapport entre la quantité de pesticides utilisée dans certains départements et la survenue de cancers.

## Creation de l'environnement virtuel sous Linux
```bash
    # Création environnement virtuel & activation
    python3 -m venv venv
    source venv/bin/activate
    # Installation librairies listées dans 'requirements.txt'
    pip install -r requirements.txt
    pip freeze
```
## Creation de l'environnement Virtuel sous windows
```shell
  # Création de l'environnement virtuel
  python -m venv venv
  # Activation de l'environnement virtuel
  .\venv\Scripts\activate
  # Installation des librairies listées dans 'requirements.txt'
  pip install -r requirements.txt
  # Affichage des librairies installées dans l'environnement virtuel
  pip freeze
```

## Déactivation de l'environnement virtuel
```
 deactivate 
```

## Le fichier .env
Les paramétres de connexion à la base de données doivent être mis dans un fichier `.env`.  
```bash
# fichier .env

USER_POSTGRES="utilisateurpostgres"
PASSWORD_POSTGRES="mdpPostgres"
HOST_POSTGRES="hostpostgresicilocalhost"
PORT_POSTGRES="serveur_port"
DATABASE_POSTGRES=postgres
SECRET_KEY="votreclésecrète"
CLIENT_MONGO=mongodb://localhost:27017/
DB_MONGO="votredbmongo"
COLLECTION_MONGO="votrecollectionmongo"
```

## Docker

```bash
    # Afficher tous les conteneurs (y compris ceux arrêtés)
    docker ps -a
    docker start <nom_du_conteneur>
    # Verifier les contenenurs lancés
    docker ps
```


## Présentation des différents dossiers

Créer un fichier Data dans lequel vous devrez télécharger les fichiers CSV indiqués dans Sources ci-dessous. 

Dans le dossier app, vous retrouverez l'application. Veuillez vous référer au README.md présent dans ce dossier pour la gestion de l'application. 

Dans le dossier doc, vous retrouverez le schéma MCD de la base de données Postgres.

Dans le dossier Rapport, vous trouverez le rapport en format docs et PDF. 

Dans le dossier Extraction, vous retrouverez plusieurs dossiers. Le premier dossier API contient le script permettant de récupérer les données provenant de l'API ainsi qu'un Notebook d'analyse.
Dans le dossier CSV, on va retrouver les notebooks d'analyse ainsi que 3 fichiers permettant d'extraire et nettoyer les données du CSV. 
Dans le dossier Metadata on retrouvera les différents scripts correspondant aux codes nécessaires pour faire le lien entre les tables ou améliorer la compréhension de certaines tables.
Dans le dossier model, on va retrouver le fichier db_init qui va intialiser la base de données. L'autre script models.py correspond aux différentes tables qui seront présents dans la base de données. 
Enfin, le dossier scrapping va comporter le script permettant de scrapper le site web et enregistrera un fichier json qui sera présent dans /data et qu'il faudra mettre dans mongoDB après.
Enfin, un fichier insertion_postgres.py va prendre en compte les scripts précédemments nommés pour mettre les informations dans Postgres. 


# Sources

Afin d'identifier les effets à plus ou moins long terme, ainsi que sur la faune et la flore de substances chimiques, j'ai récupéré les données sur le site ci-dessous :

Scrapping : https://www.sagepesticides.qc.ca/Recherche/RechercheMatiere


API : https://hubeau.eaufrance.fr/page/api-vente-et-achat-de-produits-phytopharmaceutiques#/Achat/getAchatSubstance

CSV : 
- données démographiques : https://catalogue-donnees.insee.fr/fr/catalogue/recherche/DS_ESTIMATION_POPULATION

- Données sur les pathologies : https://data.ameli.fr/explore/dataset/effectifs/table/

- Données sur l'AMM des substances et produits chimiques : https://www.data.gouv.fr/fr/datasets/donnees-ouvertes-du-catalogue-e-phy-des-produits-phytopharmaceutiques-matieres-fertilisantes-et-supports-de-culture-adjuvants-produits-mixtes-et-melanges/#/resources


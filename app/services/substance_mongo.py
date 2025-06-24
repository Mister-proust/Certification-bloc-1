from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv() # Charge les variables d'environnement depuis .env

# Récupération des informations de connexion depuis les variables d'environnement
client_mongo = os.getenv("CLIENT_MONGO")
db_mongo = os.getenv("DB_MONGO")
collection_mongo = os.getenv("COLLECTION_MONGO")

# Assurez-vous que les variables sont définies
if not client_mongo or not db_mongo or not collection_mongo:
    raise ValueError("Les variables d'environnement CLIENT_MONGO, DB_MONGO ou COLLECTION_MONGO ne sont pas définies.")

# Initialisation de la connexion MongoDB
client = MongoClient(client_mongo)
db = client[db_mongo]
collection = db[collection_mongo]

def extraire_infos(nom_produit: str):
    """
    Extrait les informations détaillées d'une substance par son nom.
    """
    doc = collection.find_one({"nom": nom_produit})
    if not doc:
        return None

    resultat = {
        "id": str(doc.get("_id")),
        "nom": doc.get("nom"),
        "url": doc.get("url"),
        "contenu_info_block": None,
        "toxicite_aigue": None,
        "effets_long_terme": None,  
        "persistance": None,
        "lessivage": None
    }

    # Récupération du contenu de l'info_block principal
    if "info_blocks" in doc and len(doc["info_blocks"]) > 0:
        resultat["contenu_info_block"] = doc["info_blocks"][0].get("contenu")

    # Accès à la toxicité aiguë et aux effets à long terme (tableau d'index 0)
    # On vérifie que le tableau existe et qu'il a au moins 1 élément (index 0)
    if len(doc.get("tableaux", [])) > 0:
        toxicite_mammiferes_block = doc["tableaux"][0].get("structure", {}).get("Toxicité chez les mammifères, incluant l'humain", {})
        
        # Récupération de la description de la toxicité aiguë
        toxicite_aigue_data = toxicite_mammiferes_block.get("Toxicité aiguë", {})
        resultat["toxicite_aigue"] = toxicite_aigue_data.get("Description des effets sur la santé")
        
        # Récupération de la description des effets à long terme
        effets_long_terme_data = toxicite_mammiferes_block.get("Effets à long terme", {})
        resultat["effets_long_terme"] = effets_long_terme_data.get("Description des effets sur la santé")

    # Accès à la persistance et au lessivage (tableau d'index 2)
    # On vérifie que le tableau existe et qu'il a au moins 3 éléments (index 0, 1, 2)
    if len(doc.get("tableaux", [])) > 2:
        devenir_environnement_block = doc["tableaux"][2].get("structure", {}).get("Devenir et comportement dans l'environnement", {})
        
        # Récupération du niveau de persistance et de sa description
        persistance_data = devenir_environnement_block.get("Persistance", {})
        resultat["persistance"] = persistance_data.get("Niveau")
        
        # Récupération du niveau de lessivage et de sa description
        lessivage_data = devenir_environnement_block.get("Potentiel de lessivage", {})
        resultat["lessivage"] = lessivage_data.get("Niveau")

    return resultat

def lister_noms_produits():
    """
    Retourne une liste triée de tous les noms de produits uniques dans la collection.
    """
    noms = sorted(list(collection.distinct("nom")))
    return noms
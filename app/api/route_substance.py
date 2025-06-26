from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from services.templates import templates
from services.authentification import get_current_user
from services.substance_mongo import extraire_infos, lister_noms_produits

# Création du router pour la gestion des substances
router = APIRouter(tags=["Exposition des substances"])

@router.get("/substance", response_class=HTMLResponse, summary="Page de sélection de substance")
async def read_substance_selector(request: Request, user=Depends(get_current_user)):
    """
    Affiche la page HTML de sélection des substances.

    Cette page permet à l'utilisateur connecté de rechercher et sélectionner une substance pour en afficher les détails.

    Paramètres :
    - request (Request) : Requête HTTP entrante.
    - user : Utilisateur actuellement connecté, vérifié via le système d'authentification.

    Retour :
    - TemplateResponse : La page HTML affichant le menu de sélection des substances.
    """
    return templates.TemplateResponse("substance.html", {"request": request, "user": user})

@router.get("/substances/noms", summary="Liste de tous les noms de substances")
def get_all_substance_names(user=Depends(get_current_user)):
    """
    Retourne la liste de toutes les substances enregistrées.

    Cette route permet d'obtenir dynamiquement les substances disponibles dans la base de données MongoDB.

    Paramètres :
    - user : Utilisateur actuellement connecté, vérifié via le système d'authentification.

    Retour :
    - dict : Dictionnaire contenant la clé 'noms' et une liste des noms de substances.
    """
    noms = lister_noms_produits()
    return {"noms": noms}

@router.get("/substances/{nom_produit}", summary="Détails d'une substance par nom")
def get_substance_details(nom_produit: str, user=Depends(get_current_user)):
    """
    Retourne les informations détaillées d'une substance spécifique.

    Paramètres :
    - nom_produit (str) : Le nom de la substance à rechercher.
    - user : Utilisateur actuellement connecté, vérifié via le système d'authentification.

    Retour :
    - dict : Détails de la substance (propriétés, caractéristiques, etc.)

    Exceptions :
    - HTTP 404 : Si la substance recherchée n'est pas trouvée.
    """
    infos = extraire_infos(nom_produit)
    if not infos:
        raise HTTPException(status_code=404, detail="Substance non trouvée.")
    return infos 
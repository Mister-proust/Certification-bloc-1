from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.templates import templates

# Création d'un router pour la page d'accueil
router = APIRouter(tags=["Accueil"])

@router.get("/", response_class=HTMLResponse, summary="Accueil de l'application d'exposition des données autour du cancer et de l'achat de pesticides.")
async def accueil(request: Request):
    """
    Affiche la page d'accueil de l'application.

    Cette page permet à l'utilisateur d'accéder aux différentes sections de l'application via une interface HTML.

    Paramètres :
    - request (Request) : La requête HTTP entrante, nécessaire pour rendre le template Jinja.

    Retour :
    - TemplateResponse : La page HTML d'accueil.
    """
    return templates.TemplateResponse("accueil.html", {"request": request})
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from services.templates import templates

router = APIRouter(tags=["Accueil"])

@router.get("/", response_class=HTMLResponse, summary="Acceuil de l'application d'exposition des données autour du cancer et de l'achat de pesticides.")
async def accueil(request: Request):
    return templates.TemplateResponse("accueil.html", {"request": request})
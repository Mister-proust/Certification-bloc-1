from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from services.templates import templates

router = APIRouter(tags=["Accueil"])

@router.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    return templates.TemplateResponse("accueil.html", {"request": request})
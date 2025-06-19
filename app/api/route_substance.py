from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from services.templates import templates
from services.authentification import get_current_user
from services.substance_mongo import extraire_infos, lister_noms_produits


router = APIRouter(tags=["Exposition des substances"])

@router.get("/substance", response_class=HTMLResponse, summary="Page de sélection de substance")
async def read_substance_selector(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("substance.html", {"request": request, "user": user})

@router.get("/substances/noms", summary="Liste de tous les noms de substances")
def get_all_substance_names(user=Depends(get_current_user)):
    noms = lister_noms_produits()
    return {"noms": noms}

@router.get("/substances/{nom_produit}", summary="Détails d'une substance par nom")
def get_substance_details(nom_produit: str, user=Depends(get_current_user)):
    infos = extraire_infos(nom_produit)
    if not infos:
        raise HTTPException(status_code=404, detail="Substance non trouvée.")
    return infos 
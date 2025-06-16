from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from Database.crud import test_fonction_sql
from services.authentification import get_current_user
from services.templates import templates

router = APIRouter(tags=["exposition_données"])

@router.get("/produits/")
def read_produits():
    return test_fonction_sql()

@router.get("/carte_france", response_class=HTMLResponse)
async def read_map(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_france.html", {"request": request, "user": user})

@router.get("/carte_france/{dept_code}", response_class=HTMLResponse)
async def show_department(request: Request, dept_code: str, user=Depends(get_current_user)):
    return HTMLResponse(content=f"<h4>Données pour le département {dept_code} </h4>")

@router.get("/carte_age", response_class=HTMLResponse)
async def carte_age(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_age.html", {"request": request, "user": user})

@router.get("/carte_sexe", response_class=HTMLResponse)
async def carte_sexe(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_sexe.html", {"request": request, "user": user})

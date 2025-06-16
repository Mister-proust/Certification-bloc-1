from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from Database.crud import test_fonction_sql
from services.authentification import get_current_user

router = APIRouter(tags=["exposition_données"])

@router.get("/produits/")
def read_produits():
    return test_fonction_sql()

@router.get("/carte_france", response_class=HTMLResponse)
async def read_map(request: Request, user=Depends(get_current_user)):
    from main import templates
    return templates.TemplateResponse("carte_france.html", {"request": request, "user": user})

@router.get("/carte_france/{dept_code}", response_class=HTMLResponse)
async def show_department(request: Request, dept_code: str, user=Depends(get_current_user)):
    return HTMLResponse(content=f"<h4>Données pour le département {dept_code} (utilisateur : {user.email})</h4>")

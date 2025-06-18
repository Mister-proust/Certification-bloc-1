from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from Database.crud import test_fonction_sql, generalite_data, graphiques_generalites, convert_decimal
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
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user)):
    data = generalite_data(dept_code, annee, type_cancer)  
    nom_departement = data[0]["nom_departement"] if data else "Inconnu"
    graph_data = graphiques_generalites(data)
    graph_data_converti = convert_decimal(graph_data)

    return templates.TemplateResponse("carte_france_generalites.html", {
        "request": request,
        "user": user,
        "dept_code": dept_code,
        "data": data,
        "annee": annee,
        "type_cancer": type_cancer,
        "nom_departement": nom_departement,
        "graph_data": graph_data_converti
    })

@router.get("/carte_age", response_class=HTMLResponse)
async def carte_age(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_age.html", {"request": request, "user": user})

@router.get("/carte_sexe", response_class=HTMLResponse)
async def carte_sexe(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_sexe.html", {"request": request, "user": user})

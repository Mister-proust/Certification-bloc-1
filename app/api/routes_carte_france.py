from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from Database.crud import generalite_data, graphiques_generalites, convert_decimal, graphiques_sexe, data_sexe, data_age, graphiques_age
from services.authentification import get_current_user
from services.templates import templates

router = APIRouter(tags=["Exposition des données"])

@router.get("/carte_france", response_class=HTMLResponse, summary="Carte de la France avec outre mer pour choisir un département.")
async def read_map(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_france.html", {"request": request, "user": user})

@router.get("/carte_france/{dept_code}", response_class=HTMLResponse, summary="Données départementales générales sur le cancer et l'achat de pesticides")
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user)):
    data = generalite_data(dept_code, annee, type_cancer)  
    data_graphique = data_sexe(dept_code)
    nom_departement = data[0]["nom_departement"] if data else "Inconnu"
    graph_data = graphiques_generalites(data_graphique)
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

@router.get("/carte_age", response_class=HTMLResponse, summary="Carte de la France avec outre mer pour choisir un département qui mènera vers des données autour des classes d'âge/le cancer et l'achat de pesticides.")
async def carte_age(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_age.html", {"request": request, "user": user})

@router.get("/carte_age/{dept_code}", response_class=HTMLResponse, summary = "Affichage des données autour des classes d'âges sur les pesticides et le cancer.")
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user), classe_age: Optional[str] = Query(None)):
    data = data_age(dept_code, annee, type_cancer, classe_age)  
    data_graphique = data_age(dept_code)
    nom_departement = data[0]["nom_departement"] if data else "Inconnu"
    graph_data = graphiques_age(data_graphique)
    graph_data_converti = convert_decimal(graph_data)

    return templates.TemplateResponse("data_age.html", {
        "request": request,
        "user": user,
        "dept_code": dept_code,
        "data": data,
        "annee": annee,
        "classe_age": classe_age,
        "type_cancer": type_cancer,
        "nom_departement": nom_departement,
        "graph_data": graph_data_converti
    })


@router.get("/carte_sexe", response_class=HTMLResponse, summary="Carte de la France avec outre mer pour choisir un département qui mènera vers des données autour des du sexe, du cancer et l'achat de pesticides.")
async def carte_sexe(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("carte_sexe.html", {"request": request, "user": user})

@router.get("/carte_sexe/{dept_code}", response_class=HTMLResponse, summary = "Données sur les achats de pesticides et la prévalence du cancer entre les hommes et les femmes.")
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user), sexe: Optional[str] = Query(None)):
    data = data_sexe(dept_code, annee, type_cancer, sexe)  
    data_graphique = data_sexe(dept_code)
    nom_departement = data[0]["nom_departement"] if data else "Inconnu"
    graph_data = graphiques_sexe(data_graphique)
    graph_data_converti = convert_decimal(graph_data)

    return templates.TemplateResponse("data_sexe.html", {
        "request": request,
        "user": user,
        "dept_code": dept_code,
        "data": data,
        "annee": annee,
        "type_cancer": type_cancer,
        "nom_departement": nom_departement,
        "graph_data": graph_data_converti
    })
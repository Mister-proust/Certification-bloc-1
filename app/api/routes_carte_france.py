from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from Database.crud import generalite_data, graphiques_generalites, convert_decimal, graphiques_sexe, data_sexe, data_age, graphiques_age
from services.authentification import get_current_user
from services.templates import templates

# Création du router pour la gestion des routes d'exposition des données
router = APIRouter(tags=["Exposition des données"])

@router.get("/carte_france", response_class=HTMLResponse, summary="Carte de la France avec outre mer pour choisir un département.")
async def read_map(request: Request, user=Depends(get_current_user)):
    """
    Affiche la page principale contenant la carte de France (y compris les DOM-TOM),
    permettant à l'utilisateur connecté de sélectionner un département.

    Paramètres :
    - request (Request) : La requête HTTP.
    - user : L'utilisateur authentifié (obtenu via dépendance).

    Retour :
    - TemplateResponse : Page HTML affichant la carte de France.
    """
    return templates.TemplateResponse("carte_france.html", {"request": request, "user": user})

@router.get("/carte_france/{dept_code}", response_class=HTMLResponse, summary="Données départementales générales sur le cancer et l'achat de pesticides")
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user)):
    """
    Affiche les données générales sur un département donné concernant le cancer
    et l'achat de pesticides, avec options de filtrage par année et type de cancer.

    Paramètres :
    - request (Request) : La requête HTTP.
    - dept_code (str) : Code du département sélectionné.
    - annee (Optional[str]) : Année pour filtrer les données (optionnel).
    - type_cancer (Optional[str]) : Type de cancer à filtrer (optionnel).
    - user : L'utilisateur authentifié.

    Retour :
    - TemplateResponse : Page HTML affichant les données générales et graphiques associés.
    """
    dept_code = str(int(dept_code))
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
    """
    Affiche la carte de France (incluant outre mer) pour choisir un département,
    avec un focus sur les données liées aux classes d'âge, cancer et pesticides.

    Paramètres :
    - request (Request) : La requête HTTP.
    - user : L'utilisateur authentifié.

    Retour :
    - TemplateResponse : Page HTML avec la carte d'âge.
    """
    return templates.TemplateResponse("carte_age.html", {"request": request, "user": user})

@router.get("/carte_age/{dept_code}", response_class=HTMLResponse, summary = "Affichage des données autour des classes d'âges sur les pesticides et le cancer.")
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user), classe_age: Optional[str] = Query(None)):
    """
    Affiche les données détaillées sur les classes d'âge dans un département donné,
    en lien avec l'achat de pesticides et la prévalence de cancers,
    avec possibilité de filtrage par année, type de cancer et classe d'âge.

    Paramètres :
    - request (Request) : La requête HTTP.
    - dept_code (str) : Code département.
    - annee (Optional[str]) : Année de filtre.
    - type_cancer (Optional[str]) : Type de cancer.
    - user : L'utilisateur authentifié.
    - classe_age (Optional[str]) : Classe d'âge à filtrer.

    Retour :
    - TemplateResponse : Page HTML avec les données et graphiques par classe d'âge.
    """
    dept_code = str(int(dept_code))
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
    """
    Affiche la carte de France (avec outre mer) permettant de choisir un département
    pour consulter des données différenciées selon le sexe,
    relatives au cancer et à l'achat de pesticides.

    Paramètres :
    - request (Request) : La requête HTTP.
    - user : L'utilisateur authentifié.

    Retour :
    - TemplateResponse : Page HTML avec la carte sexe.
    """
    return templates.TemplateResponse("carte_sexe.html", {"request": request, "user": user})

@router.get("/carte_sexe/{dept_code}", response_class=HTMLResponse, summary = "Données sur les achats de pesticides et la prévalence du cancer entre les hommes et les femmes.")
async def departement (request: Request, dept_code: str, annee: Optional[str] = Query(None), type_cancer: Optional[str] = Query(None), user=Depends(get_current_user), sexe: Optional[str] = Query(None)):
    """
    Affiche les données détaillées sur un département donné, ventilées par sexe,
    en relation avec les achats de pesticides et la prévalence du cancer,
    avec options de filtrage par année, type de cancer et sexe.

    Paramètres :
    - request (Request) : La requête HTTP.
    - dept_code (str) : Code département.
    - annee (Optional[str]) : Année pour filtrer.
    - type_cancer (Optional[str]) : Type de cancer.
    - user : L'utilisateur authentifié.
    - sexe (Optional[str]) : Sexe (homme, femme) à filtrer.

    Retour :
    - TemplateResponse : Page HTML avec les données et graphiques selon le sexe.
    """
    dept_code = str(int(dept_code))
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
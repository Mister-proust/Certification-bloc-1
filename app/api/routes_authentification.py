from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from services.templates import templates
from services.authentification import Utilisateurs, get_password_hash
from services.authentification import get_db, authenticate_user, create_access_token

# Création du router pour la gestion des routes d'authentification
router = APIRouter(tags=["Authentification"])

@router.get("/login", response_class=HTMLResponse, name="login_page", summary="Page permettant de se logger pour accéder à plus de contenus sur l'application")
async def login(request: Request, error: int=0):
    """
    Affiche la page de connexion de l'application.

    Paramètres :
    - request (Request) : Requête HTTP entrante.
    - error (int) : Code d'erreur optionnel affiché en cas d'échec de connexion.

    Retour :
    - TemplateResponse : La page HTML de connexion.
    """
    return templates.TemplateResponse("login.html", {"request": request, "nom_app": "Pesticancer", "error" : error})

@router.post("/login", summary = "Gestion de l'authentification")
async def login_for_access_token(request : Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Vérifie les identifiants de l'utilisateur et génère un token d'accès en cas de succès.

    Paramètres :
    - request (Request) : Requête HTTP entrante.
    - form_data (OAuth2PasswordRequestForm) : Formulaire contenant l'email et le mot de passe.
    - db (Session) : Session de base de données SQLAlchemy.

    Retour :
    - RedirectResponse : Redirection vers la carte si authentification réussie, sinon retour à la page de connexion avec une erreur.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        url = str(request.url_for('login_page')) + "?error=1"
        return RedirectResponse(url, status_code=302)

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    response = RedirectResponse(url="/carte_france", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/inscription", response_class=HTMLResponse, summary = "Page permettant de s'inscrire pour observer les données de l'application.")
async def register_page(request: Request):
    """
    Affiche la page d'inscription pour créer un nouveau compte.

    Paramètres :
    - request (Request) : Requête HTTP entrante.

    Retour :
    - TemplateResponse : La page HTML d'inscription.
    """
    return templates.TemplateResponse("inscription.html", {"request": request, "nom_app": "Pesticide_cancer"})

@router.post("/inscription", response_class=HTMLResponse, summary = "Requêtes nécessaire pour l'inscription")
async def register_user(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...), 
    prenom : str = Form("prenom"),
    nom : str = Form("nom"),
    date_naissance = Form("date_naissance"),
    db: Session = Depends(get_db)
):
    """
    Enregistre un nouvel utilisateur dans la base de données.

    Paramètres :
    - request (Request) : Requête HTTP entrante.
    - email (str) : Email de l'utilisateur.
    - password (str) : Mot de passe de l'utilisateur.
    - prenom (str) : Prénom de l'utilisateur.
    - nom (str) : Nom de l'utilisateur.
    - date_naissance : Date de naissance de l'utilisateur.
    - db (Session) : Session de base de données SQLAlchemy.

    Retour :
    - TemplateResponse : Redirection vers la page de connexion avec un message de succès ou une erreur si l'email existe déjà.
    """
    existing_user = db.query(Utilisateurs).filter(Utilisateurs.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "login.html", 
            {   "request": request,
                "nom_app": "Pesticancer",
                "error": True,
                "error_message": "Email existant dans la base, veuillez réessayer."
            })
    
    hashed_password = get_password_hash(password)
    new_user = Utilisateurs(email=email, hashed_password=hashed_password, prenom=prenom, nom=nom, date_naissance=date_naissance)
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "nom_app": "Pesticancer", "message": "Inscription réussie ! Vous pouvez maintenant vous connecter."}
    )

@router.get("/deconnexion", summary="Permet la déconnexion de l'utilisateur de son compte.")
async def logout():
    """
    Déconnecte l'utilisateur en supprimant le cookie contenant le token.

    Retour :
    - RedirectResponse : Redirection vers la page d'accueil.
    """
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response
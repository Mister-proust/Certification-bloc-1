from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from services.templates import templates
from services.authentification import Utilisateurs, get_password_hash
from services.authentification import get_db, authenticate_user, create_access_token


router = APIRouter(tags=["Authentification"])

@router.get("/login", response_class=HTMLResponse, name="login_page")
async def login(request: Request, error: int=0):
    return templates.TemplateResponse("login.html", {"request": request, "nom_app": "Pesticancer", "error" : error})

@router.post("/login")
async def login_for_access_token(
    request : Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
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

@router.get("/inscription", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("inscription.html", {"request": request, "nom_app": "Pesticide_cancer"})

@router.post("/inscription", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...), 
    prenom : str = Form("prenom"),
    nom : str = Form("nom"),
    date_naissance = Form("date_naissance"),
    db: Session = Depends(get_db)
):
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

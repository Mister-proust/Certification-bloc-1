from sqlalchemy import Column, Integer, String, Boolean, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from typing import Optional

# Chargement des variables d'environnement
load_dotenv(override=True)

# Configuration de la base de données et des variables de sécurité
DB_HOST = os.getenv("HOST_POSTGRES")
DB_PORT = os.getenv("PORT_POSTGRES", 5432)
DB_USER = os.getenv("USER_POSTGRES")
DB_PASS = os.getenv("PASSWORD_POSTGRES")
DB_NAME = os.getenv("DATABASE_POSTGRES")
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialisation SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Utilisateurs(Base):
    """
    Modèle de table SQLAlchemy pour les utilisateurs.
    """
    __tablename__ = "Utilisateurs"
    __table_args__ = {"schema": "Authentification"}
    
    email = Column(String, unique=True,primary_key=True, index=True)
    hashed_password = Column(String)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    last_activity = Column(Date, default=datetime.utcnow)

def create_tables():
    """
    Crée les tables dans la base de données si elles n'existent pas.
    """
    Base.metadata.create_all(bind=engine)

# Configuration du gestionnaire de mots de passe avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Vérifie qu'un mot de passe en clair correspond à son hash.

    Args:
        plain_password (str): Mot de passe fourni par l'utilisateur.
        hashed_password (str): Mot de passe hashé stocké en base.

    Retourne:
        bool: True si les mots de passe correspondent, sinon False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
     """
    Hash un mot de passe en utilisant bcrypt.

    Args:
        password (str): Mot de passe en clair.

    Retourne:
        str: Mot de passe hashé.
    """
    return pwd_context.hash(password)

def get_db():
    """
    Fournit une session SQLAlchemy pour interagir avec la base de données.

    Yields:
        Session: Instance de session active.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuration OAuth2 avec FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)

def get_user(db: Session, email: str):
    """
    Récupère un utilisateur via son email.

    Args:
        db (Session): Session SQLAlchemy.
        email (str): Email de l'utilisateur recherché.

    Retourne:
        Utilisateurs ou None: Instance de l'utilisateur ou None s'il n'existe pas.
    """
    return db.query(Utilisateurs).filter(Utilisateurs.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    """
    Authentifie un utilisateur en vérifiant son email et son mot de passe.

    Args:
        db (Session): Session SQLAlchemy.
        email (str): Email de l'utilisateur.
        password (str): Mot de passe en clair.

    Retourne:
        Utilisateurs ou None: L'utilisateur authentifié ou None si l'authentification échoue.
    """
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    user.last_activity = datetime.utcnow()
    db.commit()
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crée un token JWT d'accès pour un utilisateur.

    Args:
        data (dict): Données à encoder dans le token.
        expires_delta (timedelta, optionnel): Durée de validité du token.

    Retourne:
        str: Token JWT.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Récupère l'utilisateur actuellement connecté via le token JWT.

    Args:
        request (Request): Requête FastAPI.
        db (Session): Session SQLAlchemy.
        token (str): Token JWT récupéré via OAuth2 ou les cookies.

    Retourne:
        Utilisateurs: L'utilisateur authentifié.

    Lève:
        HTTPException: Si le token est invalide ou si l'utilisateur n'existe pas.
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Identification impossible",
        headers={"WWW-Authenticate": "Bearer"},
    )

    actual_token = token or request.cookies.get("access_token", "").removeprefix("Bearer ")

    if not actual_token:
        raise credentials_exception

    try:
        payload = jwt.decode(actual_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, email=email)
    if not user:
        raise credentials_exception
    return user

def delete_inactive_users():
    """
    Supprime les utilisateurs inactifs depuis plus d'un an.

    Cette fonction parcourt les utilisateurs et supprime ceux dont la dernière activité 
    remonte à plus d'un an.
    """
    db = SessionLocal()
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    inactive_users = db.query(Utilisateurs).filter(Utilisateurs.last_activity < one_year_ago).all()

    for user in inactive_users:
        db.delete(user)
    db.commit()
    db.close()

# Création automatique des tables lors de l'importation du fichier
create_tables()

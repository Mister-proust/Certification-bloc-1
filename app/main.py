from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
from api.routes_carte_france import router as carte_router
from api.routes_authentification import router as authentification_router
from api.route_accueil import router as accueil_router

app = FastAPI(
    title="API cancer et pesticides",
    description="Exposition des données de ventes des pesticides et des personnes atteintes de cancer par département en France",
    version="0.0.1"
)

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

sys.modules['main'].templates = templates

app.include_router(carte_router)
app.include_router(authentification_router)
app.include_router(accueil_router)
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import sys
from api.routes_carte_france import router as carte_router
from api.routes_authentification import router as authentification_router
from api.route_accueil import router as accueil_router
from api.route_substance import router as substance_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import RedirectResponse
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from services.templates import templates 
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from services.authentification import delete_inactive_users


app = FastAPI(
    title="API cancer et pesticides",
    description="Exposition des données de ventes des pesticides et des personnes atteintes de cancer par département en France",
    version="0.0.1"
)

app.mount("/static", StaticFiles(directory="./static"), name="static")

sys.modules['main'].templates = templates

app.include_router(accueil_router)
app.include_router(authentification_router)
app.include_router(carte_router)
app.include_router(substance_router)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login?error=2", status_code=302)
    raise 


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


scheduler = BackgroundScheduler()

scheduler.add_job(delete_inactive_users, 'cron', hour=0, minute=0)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
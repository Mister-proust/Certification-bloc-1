from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from services.authentification import get_current_user

router = APIRouter(tags=["exposition_substances"])

@router.get("/substance", response_class=HTMLResponse)
async def age_cancer(request:Request, dept_code : str, user=Depends(get_current_user)):
    return HTMLResponse(content=f"<h4>Données pour le département {dept_code} </h4>")
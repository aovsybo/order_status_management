from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.orders.router import get_all_requests

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/requests")
def get_all_requests(request: Request, requests=Depends(get_all_requests)):
    return templates.TemplateResponse("requests.html", {"request": request, "requests": requests})


@router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

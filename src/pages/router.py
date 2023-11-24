from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.auth.base_config import current_user
from src.auth.models import User


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get("/chat")
def get_chat_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("chat.html", {"request": request, "user": user})

"""
Модуль для главной страницы сервер и страницы о программе
"""
import sqlalchemy
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import fastapi
router_pages = APIRouter()

templates = Jinja2Templates(directory="templates")


@router_pages.get("/")
async def get_index_page(request: Request):
    """
    Главная страница
    :param request:
    :return:
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router_pages.get("/about")
async def get_about_page(request: Request):
    """
    Страница о программе
    :param request:
    :return:
    """
    return templates.TemplateResponse("about.html",
                                      {"request": request,
                                       "soft_version": f"1.1."
                                                       f"FastAPI {fastapi.__version__}, "
                                                       f"Sqlalchemy {sqlalchemy.__version__}"
                                       }
                                      )

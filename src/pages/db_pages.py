from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
import datetime
from pydantic import BaseModel

from model.database import SessionLocal, requests_table

# from model.database import requests_table, database, SessionLocal

db_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@db_router.get("/show")
async def show_records(request: Request):
    db = SessionLocal()
    records = db.query(requests_table).all()
    return templates.TemplateResponse("show.html", {"request": request, "records": records})

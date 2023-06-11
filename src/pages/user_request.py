from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
import datetime
from pydantic import BaseModel

from model.database import requests_table, database, SessionLocal
from predict.predict import get_category

user_router = APIRouter()
templates = Jinja2Templates(directory="templates")


class SupportRequest(BaseModel):
    """
    Модель данных для параметров запроса
    """
    name: str
    email: str
    message: str


@user_router.get("/show")
async def show_records(request: Request):
    db = SessionLocal()
    records = db.query(requests_table).all()
    return templates.TemplateResponse("show.html", {"request": request, "records": records})


@user_router.post("/request")
async def create_request(request: SupportRequest):
    print(f"name = {request.name}, email: {request.email}, message = {request.message}")

    category = get_category(request.message)

    print(f"category = {category}")

    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    query = requests_table.insert().values(
        date=date,
        name=request.name,
        email=request.email,
        message=request.message,
        category=category,
        status="в работе",
    )

    request_id = await database.execute(query)
    return \
        {
            "id": request_id,
            **request.dict(),
            "date": date,
            "category": category,
            "status": "в работе"
        }


@user_router.post("/delete_record")
async def delete_record(request: Request):
    # Получаем идентификатор записи из тела запроса
    data = await request.json()
    record_id = data['record_id']

    # Получаем соединение с базой данных и удаляем запись
    db = SessionLocal()
    db.query(requests_table).filter(requests_table.c.id == record_id).delete()
    db.commit()

    # Возвращаем перенаправление на главную страницу
    records = db.query(requests_table).all()
    return templates.TemplateResponse("index.html", {"request": request, "records": records})


# функция для получения списка всех обращений в поддержку
@user_router.get("/requests/")
async def read_requests():
    query = requests_table.select()
    return await database.fetch_all(query)


# функция для получения информации об одном обращении в поддержку по id
@user_router.get("/requests/{request_id}")
async def read_request(request_id: int):
    query = requests_table.select().where(requests_table.c.id == request_id)
    request = await database.fetch_one(query)
    if request is None:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    return request


# функция для обновления статуса обращения в поддержку
@user_router.put("/requests/{request_id}")
async def update_request(request_id: int, status: str):
    query = (
        requests_table.update()
        .where(requests_table.c.id == request_id)
        .values(status=status)
    )
    updated_rows = await database.execute(query)
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    return {"status": status}

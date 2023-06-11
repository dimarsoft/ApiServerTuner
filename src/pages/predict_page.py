"""
Модуль для главной страницы сервер и страницы о программе
"""
import datetime

from fastapi import APIRouter, UploadFile, File
from fastapi.templating import Jinja2Templates

from predict.predict import predict_request_sync, predict_request_async
from predict.time_tools import time_synch, time_elapsed
from model.database import requests_table, database, SessionLocal

predict_pages = APIRouter()

templates = Jinja2Templates(directory="templates")


@predict_pages.post('/image_predict_async')
async def image_predict_async(image: UploadFile = File(...)):
    start_time = time_synch()

    print(f"start_time = {start_time}")

    answer = await predict_request_async(image)

    end_time = time_synch()

    print(f"end_time = {end_time}")

    elapsed = time_elapsed(start_time, end_time)

    print(f"elapsed = {elapsed}")

    answer["time_elapsed"] = str(elapsed)
    answer["start_time"] = str(start_time)
    answer["end_time"] = str(end_time)

    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    query = requests_table.insert().values(
        date=date,
        mode="async",
        time_elapsed=str(elapsed),
        file=image.filename,
        image_class=answer["class"],
        start_time=str(start_time),
        end_time=str(end_time)
    )

    request_id = await database.execute(query)

    answer["request_id"] = str(request_id)

    return answer


@predict_pages.post('/image_predict_sync')
async def image_predict_sync(image: UploadFile = File(...)):
    start_time = time_synch()

    print(f"start_time = {start_time}")

    answer = predict_request_sync(image)

    end_time = time_synch()

    print(f"end_time = {end_time}")

    elapsed = time_elapsed(start_time, end_time)

    print(f"elapsed = {elapsed}")

    answer["time_elapsed"] = str(elapsed)
    answer["start_time"] = str(start_time)
    answer["end_time"] = str(end_time)

    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    query = requests_table.insert().values(
        date=date,
        mode="sync",
        image_class=answer["class"],
        time_elapsed=str(elapsed),
        file=image.filename,
        start_time=str(start_time),
        end_time=str(end_time)
    )

    request_id = await database.execute(query)

    answer["request_id"] = str(request_id)

    return answer

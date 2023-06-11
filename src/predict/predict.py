import time

from tensorflow.keras.models import load_model
import io
from pathlib import Path

import numpy as np
from PIL import Image
import gdown
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool

classes = {0: 'самолет',
           1: 'автомобиль',
           2: 'птица',
           3: 'кот',
           4: 'олень',
           5: 'собака',
           6: 'лягушка',
           7: 'лошадь',
           8: 'корабль',
           9: 'грузовик'}


def download_model():
    cloud_path = 'https://storage.yandexcloud.net/aiueducation/Content/base/l6/model_fmr_all.h5'

    file_path = Path("./static/model_text_bow_dense.h5")

    if not file_path.exists():
        # Загрузка датасета из облака
        gdown.download(cloud_path, output=str(file_path), quiet=False)
    model_category = load_model(file_path)

    return model_category


model = download_model()


def run_predict(image):
    prediction = model.predict(image)

    time.sleep(1)

    class_id = np.argmax(prediction)

    return class_id


def predict_image(image) -> str:
    image = Image.open(io.BytesIO(image))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((32, 32))
    image = np.array(image, dtype='float64') / 255
    image = np.expand_dims(image, axis=0)

    class_id = run_predict(image)

    return classes[int(class_id)]


async def predict_request_async(request: UploadFile) -> dict[str, str]:
    if request.file:
        image = await request.read()
        image = Image.open(io.BytesIO(image))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((32, 32))
        image = np.array(image, dtype='float64') / 255
        image = np.expand_dims(image, axis=0)

        class_id = await run_in_threadpool(run_predict, image)

        return {'class': classes[int(class_id)]}

    return {'error': 'No image provided'}


def predict_request_sync(request: UploadFile) -> dict[str, str]:
    if request.file:
        image = request.file.read()
        image = Image.open(io.BytesIO(image))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((32, 32))
        image = np.array(image, dtype='float64') / 255
        image = np.expand_dims(image, axis=0)

        class_id = run_predict(image)

        return {'class': classes[int(class_id)]}

    return {'error': 'No image provided'}

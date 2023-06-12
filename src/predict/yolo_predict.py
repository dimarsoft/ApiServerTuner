"""
Модуль для классификации изображения.
Используется обученная модель yolov8n-cls.pt
"""
import io

import torch
from PIL import Image
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")


def predict_yolo(image) -> tuple[int, str, float]:
    """
    Классификация изображения
    :param image:
    :return:
        tuple[int, str, float]: Класс, название, вероятность
    """
    results = model.predict(image)
    probs = results[0].probs.data
    class_id = int(torch.argmax(probs))

    conf = float(probs[class_id])

    class_name = results[0].names[int(class_id)]

    return class_id, class_name, conf


def predict_yolo_bytes(image) -> tuple[int, str, float]:
    image = Image.open(io.BytesIO(image))
    if image.mode != "RGB":
        image = image.convert("RGB")

    return predict_yolo(image)


async def predict_request_yolo(request: UploadFile) -> dict[str, str]:
    if request.file:
        image = request.file.read()
        image = Image.open(io.BytesIO(image))
        if image.mode != "RGB":
            image = image.convert("RGB")

        class_id, class_name, conf = await run_in_threadpool(predict_yolo, image)

        return {
            "class_id": str(class_id),
            "class": class_name,
            "conf": str(conf)
        }


def run():
    """
    Отладка локально
    :return:
    """
    class_id, class_name, conf = predict_yolo("C:\\AI\\my_phos\\test_images\\6.jpg")

    print(f"class_name = {class_name}, id = {class_id}, conf = {conf}")


if __name__ == '__main__':
    run()

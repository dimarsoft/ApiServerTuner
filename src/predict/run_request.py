from pathlib import Path
from threading import Thread
from typing import List

import requests

from time_tools import time_synch, time_elapsed


def run(path_to_image, url: str):
    files = {'image': open(path_to_image, 'rb')}

    start_time = time_synch()

    print(f"start_time = {start_time}")

    response = requests.post(url, files=files)

    end_time = time_synch()

    print(f"end_time = {end_time}")

    elapsed = time_elapsed(start_time, end_time)

    print(f"elapsed = {elapsed}")

    json_response = "empty"

    if response.status_code == 200:
        print('File uploaded successfully')
        json_response = response.json()
        print('Response:', json_response)
    else:
        print('File upload failed')

    answer = {
        "status_code": str(response.status_code),
        "json_response": str(json_response),
        "time_elapsed": str(elapsed),
        "start_time": str(start_time),
        "end_time": str(end_time)}

    return answer


def run_in_folder(folder: str, url: str, trials: int = 10):
    folder = Path(folder)

    for trial in range(trials):

        for entry in folder.iterdir():
            file = str(entry)
            ans = run(file, url)

            print(f"{trial}. file {file}, {ans}")


def run_in_folder_th(folder: str, url: str, trials: int = 10):
    folder = Path(folder)

    threads: List[Thread] = []

    for i in range(trials):
        threads.append(Thread(target=run_in_folder, args=(folder, url, trials)))

    for trial in threads:
        trial.start()

    for trial in threads:
        trial.join()


def example():
    url = "http://127.0.0.1:5010/predict"
    url = "http://127.0.0.1:5020/image_predict_sync"
    url = "http://127.0.0.1:5020/image_predict_async"
    folder = "C:\\AI\\my_phos"

    run_in_folder_th(folder, url)


example()

import datetime
from pathlib import Path
from threading import Thread
from typing import List
import csv
import requests

from time_tools import time_synch, time_elapsed


def run(path_to_image, url: str):
    files = {'image': open(path_to_image, 'rb')}

    start_time = time_synch()

    # print(f"start_time = {start_time}")

    response = requests.post(url, files=files)

    end_time = time_synch()

    # print(f"end_time = {end_time}")

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
        "time_elapsed": elapsed,
        "start_time": str(start_time),
        "end_time": str(end_time)}

    return answer


def run_in_folder(folder: str, url: str, trials: int = 10, tag: str = ""):
    folder = Path(folder)

    date = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

    filename = str(folder / "csv" / f"{date}_{tag}.csv")

    with open(filename, "w", newline='') as file_txt:
        # Write the text to the file
        writer = csv.writer(file_txt, delimiter=";")
        for trial in range(trials):
            for entry in folder.iterdir():
                if not entry.is_file():
                    continue
                file = str(entry)
                ans = run(file, url)

                time_elapsed_str = ans["time_elapsed"]

                print(f"{trial}. file {file}, {tag}, elapsed = {time_elapsed_str}c")

                # file_txt.write(f"{file};{time_elapsed_str}\n")

                writer.writerow([file, time_elapsed_str])

                file_txt.flush()


def run_in_folder_th(folder: str, url: str, trials: int = 10, tag: str = ""):
    folder = Path(folder)

    threads: List[Thread] = []

    for i in range(trials):
        threads.append(Thread(target=run_in_folder, args=(folder, url, trials, f"tag_{tag}_{i}")))

    for trial in threads:
        trial.start()

    for trial in threads:
        trial.join()


def example():
    url_flask = "http://127.0.0.1:5010/predict"
    url_flask_sync = "http://127.0.0.1:5010/predict_sync"
    url_flask_sync = "http://84.201.162.106:8000/predict"
    url_sync = "http://127.0.0.1:5020/image_predict_sync"

    url_async = "http://127.0.0.1:5020/image_predict_async"
    url_fastapi_async = "http://84.201.162.106:8000/image_predict_async"
    url_fastapi_sync = "http://84.201.162.106:8000/image_predict_sync"

    # folder = "C:\\AI\\my_phos"
    folder = "C:\\AI\\my_phos\\test_images"

    # run_in_folder_th(folder, url_async, 2, "async")
    # run_in_folder_th(folder, url_sync, 2, "sync")
    # run_in_folder_th(folder, url_flask_sync, 10, "flask_sync")
    # run_in_folder_th(folder, url_fastapi_async, 10, "fastapi_async")

    # run_in_folder_th(folder, url_fastapi_sync, 10, "fastapi_sync")
    # run_in_folder_th(folder, url_flask_sync, 10, "flask_sync")

    url_sync_yolo = "http://127.0.0.1:5020/image_predict_yolo"

    run_in_folder_th(folder, url_sync_yolo, 10, "async_yolo")

example()

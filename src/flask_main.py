"""
Основной модуль для приложения на Flask
"""

import flask
import sqlalchemy
from flask import Flask, render_template, request, jsonify

from model.database import SessionLocal, requests_table
from predict.predict import predict_image
from predict.time_tools import time_synch, time_elapsed
from predict.yolo_predict import predict_yolo

app = Flask(__name__, template_folder='templates/flask')


@app.route('/')
def view_main():
    return render_template("index.html")


@app.route('/about')
def view_about():
    soft_version = f"1.1." \
                   f"Flask {flask.__version__}, " \
                   f"Sqlalchemy {sqlalchemy.__version__}"

    return render_template("about.html", soft_version=soft_version)


@app.get("/show")
def show_records():
    db = SessionLocal()
    records = db.query(requests_table).all()
    return render_template("show.html", records=records)


@app.route('/predict', methods=['POST'])
def predict():
    if request.files.get('image'):
        start_time = time_synch()

        print(f"start_time = {start_time}")

        # filename = request.files['image'].filename
        image = request.files['image'].read()

        class_str = predict_image(image)

        end_time = time_synch()

        print(f"end_time = {end_time}")

        elapsed = time_elapsed(start_time, end_time)

        print(f"elapsed = {elapsed}")

        answer = \
            {
                "class": class_str,
                "time_elapsed": str(elapsed),
                "start_time": str(start_time),
                "end_time": str(end_time)
            }

        return jsonify(answer)

    return jsonify({'error': 'No image provided'}), 400


@app.route('/predict_yolo', methods=['POST'])
def predict_yolo_endpoint():
    if request.files.get('image'):
        start_time = time_synch()

        print(f"start_time = {start_time}")

        # filename = request.files['image'].filename
        image = request.files['image'].read()

        class_id, class_str, conf = predict_yolo(image)

        end_time = time_synch()

        print(f"end_time = {end_time}")

        elapsed = time_elapsed(start_time, end_time)

        print(f"elapsed = {elapsed}")

        answer = \
            {
                "class": class_str,
                "class_id": str(class_id),
                "conf": str(conf),
                "time_elapsed": str(elapsed),
                "start_time": str(start_time),
                "end_time": str(end_time)
            }

        return jsonify(answer)

    return jsonify({'error': 'No image provided'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)

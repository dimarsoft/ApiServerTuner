"""
Основной модуль для приложения на Flask
"""
import datetime

import flask
import sqlalchemy
from flask import Flask, render_template, request, jsonify

from model.database import SessionLocal, requests_table, database
from predict.predict import predict_image
from predict.time_tools import time_synch, time_elapsed

app = Flask(__name__, template_folder='templates/flask')


@app.route('/')
def view_main():
    return render_template("index.html")


@app.route('/about')
async def view_about():
    soft_version = f"1.1." \
                   f"Flask {flask.__version__}, " \
                   f"Sqlalchemy {sqlalchemy.__version__}"

    return render_template("about.html", soft_version=soft_version)


@app.get("/show")
async def show_records():
    db = SessionLocal()
    records = db.query(requests_table).all()
    return render_template("show.html", records=records)


@app.route('/predict', methods=['POST'])
async def predict():
    if request.files.get('image'):
        start_time = time_synch()

        print(f"start_time = {start_time}")

        filename = request.files['image'].filename
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
                "end_time": str(end_time)}

        date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        query = requests_table.insert().values(
            date=date,
            mode="sync",
            image_class=answer["class"],
            time_elapsed=str(elapsed),
            file=filename,
            start_time=str(start_time),
            end_time=str(end_time)
        )

        request_id = await database.execute(query)

        answer["request_id"] = str(request_id)

        return jsonify(answer)

    return jsonify({'error': 'No image provided'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)

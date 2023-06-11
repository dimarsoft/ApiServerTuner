"""
Основной модуль для приложения на Flask
"""
import flask
import sqlalchemy
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates/flask')


@app.route('/')
def view_main():
    return render_template("index.html")


@app.route('/about')
def view_about():
    soft_version = f"1.1."\
                   f"Flask {flask.__version__}, "\
                   f"Sqlalchemy {sqlalchemy.__version__}"

    return render_template("about.html", soft_version=soft_version)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)

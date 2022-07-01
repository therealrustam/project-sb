import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

UPLOAD_FOLDER = 'd:/Dev/project-sb/download'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1ZakonOma@localhost/db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class DataModel(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    delta = db.Column(db.Float())

    def __init__(self, date, delta):
        self.date = date
        self.delta = delta

    def __repr__(self):
        return f""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return download_file()
    return '''
    <!doctype html>
    <title>Загрузка вашего файла</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: #f0f8ff;
            background-color: #070217;
            font-size: 24px;
            font-family: Helvetica, sans-serif;
        }
        </style>
    <body>
    <h1>Загрузка вашего файла</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Загрузить>
    </form>
    </body>
    '''


@app.route('/download/', methods=['GET'])
def download_file():
    return '''
    <!doctype html>
    <title>Загружено</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: #f0f8ff;
            background-color: #070217;
            font-size: 24px;
            font-family: Helvetica, sans-serif;
        }
        </style>
    <body>
    <h1>Загружено</h1>
    </body>
    '''


if __name__ == '__main__':
    app.run(debug=True)

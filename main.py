import os

import pandas as pd
from dateutil import parser
from flask import (Flask, flash, jsonify, redirect, request)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook
from sqlalchemy import MetaData, Table, create_engine, select
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './download'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'
           ] = 'postgresql://postgres:1ZakonOma@localhost/db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)

metadata = MetaData()
engine = create_engine('postgresql://postgres:1ZakonOma@localhost/db')


class DataModel(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    delta = db.Column(db.Float())

    def __init__(self, date, delta):
        self.date = date
        self.delta = delta

    def __repr__(self):
        return f"{self.id}"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
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


@app.route('/import/xlsx/', methods=['GET'])
def import_file():
    dataset = DataModel.query.filter_by().all()
    if dataset:
        for object in dataset:
            db.session.delete(object)
            db.session.commit()
        return jsonify(
            result=0,
            message='Данные из БД удалены'
        )
    wb = load_workbook('./download/testData.xlsx')
    sheet = wb.get_sheet_by_name('Лист1')
    amount = sheet.max_row
    for counter in range(2, amount+1):
        date_string = sheet.cell(row=counter, column=1).value
        datetime_object = parser.parse(date_string)
        delta = float(
            str(sheet.cell(row=counter, column=2).value).replace(',', '.'))
        data = DataModel(datetime_object, delta)
        db.session.add(data)
        db.session.commit()
    return jsonify(
        amount=amount-1,
        message='Данные введены в БД'
    )


@app.route('/export/sql/', methods=['GET'])
def export_json():
    dataset = Table('data-view', metadata, autoload_with=engine)
    stmt = select(dataset)
    connection = engine.connect()
    dataset = connection.execute(stmt).fetchall()
    if dataset:
        date_list = {}
        delta_list = {}
        deltalag_list = {}
        lag_num_list = {}
        counter = 1
        for object in dataset:
            date = object.date.strftime('%d.%m.%Y')
            delta = object.delta
            deltalag = 0 if object.deltalag is None else object.deltalag
            lag_num = abs(object.delta - (
                float(0 if object.deltalag is None else object.deltalag)))
            date_list[counter] = date
            delta_list[counter] = delta
            deltalag_list[counter] = deltalag
            lag_num_list[counter] = lag_num
            counter += 1
        return jsonify(
            message='OK',
            date=date_list,
            delta=delta_list,
            deltalag=deltalag_list,
            lag_num=lag_num_list,
        )
    return jsonify(
        data=0,
        message='Данные отстутсвуют'
    )


@ app.route('/export/pandas/', methods=['GET'])
def export_pandas():
    dataset = DataModel.query.filter_by().all()
    if dataset:
        date_list = []
        delta_list = []
        for object in dataset:
            date_list.append(object.date)
            delta_list.append(object.delta)
        df = pd.DataFrame({'date': date_list,
                           'delta': delta_list})
        df = df.sort_values(by='date')
        df['DeltaLag'] = (df['delta'].shift(2, fill_value=0))
        df['lag_num'] = (df['delta']-df['DeltaLag']).abs()
        return df.to_json(path_or_buf=None, date_format='iso')
    return jsonify(
        data=0,
        message='Данные отстутсвуют'
    )


if __name__ == '__main__':
    app.run(debug=True)

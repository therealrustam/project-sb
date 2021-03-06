# Тестовое задание Project SB


## Описание

Данная программа представляет собой Микросервис на архитектуре **REST API** со следующим функционалом:
- загрузка файла в формате *.xlsx на сервер;
- импорт данных из файла в формате *.xlsx в Базу Данных;
- выдачу данных из SQL-таблицы в формате JSON.

Программа создана на основе фреймворка **Flask** языка программирования **Python**. В качестве БД используется реляционная База Данных **PostgreSQL**. Все запросы Сервис принимает в виде REST запросов по протоколу HTTP.


## Установка

- Клонируйте новый репозиторий себе на компьютер.
- Разверните в репозитории виртуальное окружение: в папке скачанного репозитория выполните команду: `python -m venv venv`.
- Активируйте виртуальное окружение: `source venv/Scripts/activate`.
- В виртуальном окружении установите зависимости: `pip install -r requirements.txt`.
- Для определения переменной среды, которая определяет сценарий, в котором размещается наше приложение Flask: `export FLASK_APP=main.py`
- Для создания таблицы data в нашей базе данных: `flask db init`, `flask db migrate`, `flask db upgrade`.
- Для запуска программы введите команду: `flask run`.


## Стек технологии

- alembic==1.8.0
- autopep8==1.6.0
- click==8.1.3
- colorama==0.4.5
- et-xmlfile==1.1.0
- flake8==4.0.1
- Flask==2.1.2
- Flask-Migrate==3.1.0
- Flask-SQLAlchemy==2.5.1
- greenlet==1.1.2
- importlib-metadata==4.2.0
- importlib-resources==5.8.0
- itsdangerous==2.1.2
- Jinja2==3.1.2
- Mako==1.2.1
- MarkupSafe==2.1.1
- mccabe==0.6.1
- numpy==1.21.6
- openpyxl==3.0.10
- pandas==1.1.5
- psycopg2-binary==2.9.3
- pycodestyle==2.8.0
- pyflakes==2.4.0
- python-dateutil==2.8.2
- pytz==2022.1
- six==1.16.0
- SQLAlchemy==1.4.39
- toml==0.10.2
- typing_extensions==4.2.0
- Werkzeug==2.1.2
- zipp==3.8.0


## Примеры

Примеры запросов по API:

- [GET] /import/xlsx/ - Если таблица в базе есть, она очищается, иначе – создается. Импортируемые данные приводятся к формату SQL-таблицы и загружаются в базу.
- [GET]  /export/sql/ - При каждом запросе по данному URL сервис делает SQL запрос к Представлению и отдает все данные в формате JSON.
- [GET] /export/pandas/ -  При каждом запросе по данному URL сервис делает SQL запрос к БД и отдает все данные в формате JSON.


## SQL код для создания VIEW Представления

```
CREATE OR REPLACE VIEW data-view AS
WITH result_data AS (
         SELECT data.date,
            data.delta
           FROM data
          ORDER BY data.date
        )
 SELECT result_data.date,
    result_data.delta,
    lag(result_data.delta, 2) OVER 
    (ORDER BY result_data.date) AS deltalag
   FROM result_data;
```

## Авторы

Вахитов Рустам

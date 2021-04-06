import csv

from sqlalchemy.orm.exc import NoResultFound

from app.database.models import db, InputData, FinancialData
from datetime import date

from app.scraper.coingecko.cg_service import CgService

cg = CgService()

def populate_db_api(row, source):
    today = date.today()
    try:
        existing = db.session.query(InputData).filter_by(name=row['name']).one()
        existing.order = row['id']
        string_id = find_string_id(existing.name)
        existing.string_id = string_id

    except NoResultFound:
        new_input_data = InputData(order=row['id'], name=row['name'], ticker=row['ticker'],
                                   date=today, source=source)
        string_id = find_string_id(new_input_data.name)
        new_input_data.string_id = string_id
        db.session.add(new_input_data)

    db.session.commit()

def find_string_id(name):
    string_id = cg.find_id(name)
    if string_id is not None:
        return string_id
    else:
       return name

def populate_db_from_csv():
    csv_url = "./app/utility/cryptocurrencies_2021-02-20.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            today = date.today()
            source = 'csv'
            new_record = InputData(order=row['id'], name=row['name'], ticker=row['ticker'], date=today, source=source)
            db.session.add(new_record)
            db.session.commit()


def update_populate_db():
    csv_url = "./app/utility/cryptocurrencies_2021-02-27.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            today = date.today()
            source = 'csv'
            new_record = InputData(order=row['id'], name=row['name'], ticker=row['ticker'],
                                   price=row['price'], market_cap=row['market_cap'], date=today, source=source)
            try:
                existing = db.session.query(InputData).filter_by(name=row['name']).one()
                existing.price = row['price']
                existing.market_cap = row['market_cap']

            except NoResultFound:
                new_record = InputData(order=row['id'], name=row['name'], ticker=row['ticker'],
                                       price=row['price'], market_cap=row['market_cap'], date=today, source=source)
                db.session.add(new_record)
            db.session.commit()

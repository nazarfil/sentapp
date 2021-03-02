import csv

from sqlalchemy.orm.exc import NoResultFound

from app.models import db, InputData
from datetime import date


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


def populate_db_api(row):
    today = date.today()
    source = 'api'
    try:
        existing = db.session.query(InputData).filter_by(name=row['name']).one()
        existing.price = row['price']
        existing.market_cap = row['market_cap']
        existing.source=source
    except NoResultFound:
        new_record = InputData(order=row['id'], name=row['name'], ticker=row['ticker'],
                               price=row['price'], market_cap=row['market_cap'], date=today, source=source)
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

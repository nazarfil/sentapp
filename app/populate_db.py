import csv
from .models import db, InputData
from datetime import date


def populate_db():
    csv_url = "./app/utility/cryptocurrencies_2021-02-20.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            today = date.today()
            source = 'csv'
            new_record = InputData(order=row['id'], name=row['name'], ticker=row['ticker'], date=today, source=source)
            db.session.add(new_record)
            db.session.commit()

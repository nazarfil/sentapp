from app.database.models import SentimentScore, db, InputData, SentimentHypeScore
from sqlalchemy.sql import func
import csv
import logging

from app.utility.formats import foramt_Y_M_D



def calculate_hype_score(date, input_data_id):
    logging.info("Calculating hype score for {}".format(input_data_id))
    sum_positive = (db.session.query(func.sum(SentimentScore.positive).label('positive'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(),
                    "POSITIVE")
    sum_negative = (db.session.query(func.sum(SentimentScore.negative).label('negative'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(),
                    "NEGATIVE")

    sum_mixed = (db.session.query(func.sum(SentimentScore.mixed).label('mixed'))
                 .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(), "MIXED")
    count_today = SentimentScore.query.filter_by(input_data=input_data_id, date=date).count()

    if (sum_positive[0][0] is not None) and (sum_negative[0][0] is not None) and (sum_mixed[0][0] is not None):
        absolute_hype = sum_positive[0].positive + sum_mixed[0].mixed - sum_negative[0].negative
        relative_hype = (sum_positive[0].positive + sum_mixed[0].mixed) / sum_negative[0].negative
        hype_record = SentimentHypeScore(
            input_data=input_data_id,
            absolute_hype=absolute_hype,
            relative_hype=relative_hype,
            count=count_today,
            date=date
        )
        existing = db.session.query(SentimentHypeScore).filter_by(input_data=input_data_id, date=date).first()
        if existing is None:
            db.session.add(hype_record)
            db.session.commit()


def hype_score_from_csv():
    csv_url = "app/jobs/populate.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            input_data = InputData.query.filter_by(name=row["name"]).one()
            if input_data is not None:
                calculate_hype_score(date=row["date"], input_data_id=input_data)


def hype_score_for_coin(name, date):
    input_data = InputData.query.filter_by(name=name).one()
    if input_data is not None:
        calculate_hype_score(date=date, input_data_id=input_data)


def hype_score_for_all_coins():
    input_data_ids = db.session.query(SentimentScore.input_data.distinct()).all()
    for data_id in input_data_ids:
        dates = db.session.query(SentimentScore.date.distinct()).filter_by(input_data=data_id[0]).all()
        for date in dates:
            date_str = date[0].strftime(foramt_Y_M_D)
            calculate_hype_score(date_str, input_data_id=data_id[0])

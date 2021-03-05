from app.models import SentimentMeanScore, SentimentScore, db, InputData, SentimentHypeScore
from sqlalchemy.sql import func
from operator import itemgetter
import csv, datetime

from app.utility.formats import foramt_Y_M_D


def calculate_mean_score(date, in_name):
    print("CALCULATING MEAN SCORE")
    input_data = InputData.query.filter_by(name=in_name).first()
    avg_positive = (db.session.query(func.avg(SentimentScore.positive).label('positive'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data.id).first(),
                    "POSITIVE")
    avg_negative = (db.session.query(func.avg(SentimentScore.negative).label('negative'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data.id).first(),
                    "NEGATIVE")
    avg_neutral = (db.session.query(func.avg(SentimentScore.neutral).label('neutral'))
                   .filter(SentimentScore.date == date, SentimentScore.input_data == input_data.id).first(), "NEUTRAL")
    avg_mixed = (db.session.query(func.avg(SentimentScore.mixed).label('mixed'))
                 .filter(SentimentScore.date == date, SentimentScore.input_data == input_data.id).first(), "MIXED")
    list_avg = [avg_positive, avg_mixed, avg_neutral, avg_negative]
    avh_res = max(list_avg, key=itemgetter(0))

    return SentimentMeanScore(
        input_data=input_data.id,
        sentiment=avh_res[1],
        positive=avg_positive[0],
        negative=avg_negative[0],
        neutral=avg_neutral[0],
        mixed=avg_mixed[0],
        date=date,
        source="AWS")


def mean_score_from_csv():
    csv_url = "app/jobs/populate.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            mean_score = calculate_mean_score(date=row["date"], in_name=row["name"])
            db.session.add(mean_score)
            db.session.commit()


def calculate_hype_score(date, input_data_id):
    print("CALCULATING HYPE SCORE for", input_data_id)
    yesterday = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
    sum_positive = (db.session.query(func.sum(SentimentScore.positive).label('positive'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(),
                    "POSITIVE")
    sum_negative = (db.session.query(func.sum(SentimentScore.negative).label('negative'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(),
                    "NEGATIVE")
    sum_neutral = (db.session.query(func.sum(SentimentScore.neutral).label('neutral'))
                   .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(), "NEUTRAL")
    sum_mixed = (db.session.query(func.sum(SentimentScore.mixed).label('mixed'))
                 .filter(SentimentScore.date == date, SentimentScore.input_data == input_data_id).first(), "MIXED")
    count_today = SentimentScore.query.filter_by(input_data=input_data_id, date=date).count()
    count_yesterday = SentimentScore.query.filter_by(input_data=input_data_id,
                                                     date=yesterday.strftime('%Y-%m-%d')).count()
    delta = count_today - count_yesterday
    if (sum_positive[0][0] is not None) and (sum_negative[0][0] is not None) and (sum_mixed[0][0] is not None):
        absolute_hype = sum_positive[0].positive + sum_mixed[0].mixed - sum_negative[0].negative
        relative_hype = (sum_positive[0].positive + sum_mixed[0].mixed) / sum_negative[0].negative
        hype_record = SentimentHypeScore(
            input_data=input_data_id,
            absolute_hype=absolute_hype,
            relative_hype=relative_hype,
            delta_tweets=delta,
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

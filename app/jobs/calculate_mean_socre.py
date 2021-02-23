from app.models import SentimentMeanScore, SentimentScore, db, InputData
from sqlalchemy.sql import func
from operator import itemgetter
import csv


def calculate_mean_score(date, in_name):
    input_data = InputData.query.filter_by(name=in_name).first()
    avg_positive = (db.session.query(func.avg(SentimentScore.positive).label('average'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data.id).first(), "POSITIVE")
    avg_negative = (db.session.query(func.avg(SentimentScore.negative).label('negative'))
                    .filter(SentimentScore.date == date, SentimentScore.input_data == input_data.id).first(), "NEGATIVE")
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

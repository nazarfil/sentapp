from datetime import datetime, timedelta

from app.database.models import SentimentScore, db, InputData, SentimentHypeScore
from sqlalchemy.sql import func

import app.log as log

logger = log.def_logger


def get_yesterday_data(date, input_data_id):
    yesterday = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)

    try:
        yesterday_score = SentimentHypeScore.query.filter_by(input_data=input_data_id,
                                                             date=yesterday.strftime('%Y-%m-%d')).first()
        count_yesterday = yesterday_score.count
        rel_hype_yesterday = yesterday_score.relative_hype
        abs_hype_yesterday = yesterday_score.absolute_hype
        return count_yesterday, rel_hype_yesterday, abs_hype_yesterday
    except:
        logger.error("No data for yesterday")
        return 1, 1, 1


def calculate_hype_score(date, input_data_id):

    tomorrow = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
    sum_positive = db.session.query(func.sum(SentimentScore.positive).label('sum')).filter(SentimentScore.date > date,SentimentScore.date < tomorrow,
                                                                                           SentimentScore.input_data == input_data_id).one()
    sum_negative = db.session.query(func.sum(SentimentScore.negative).label('sum')).filter(SentimentScore.date > date,SentimentScore.date < tomorrow,
                                                                                           SentimentScore.input_data == input_data_id).one()
    sum_neutral = db.session.query(func.sum(SentimentScore.neutral).label('sum')).filter(SentimentScore.date > date,SentimentScore.date < tomorrow,
                                                                                         SentimentScore.input_data == input_data_id).one()
    sum_mixed = db.session.query(func.sum(SentimentScore.mixed).label('sum')).filter(SentimentScore.date > date,SentimentScore.date < tomorrow,
                                                                                     SentimentScore.input_data == input_data_id).one()

    count_today =  db.session.query(SentimentScore).filter(SentimentScore.date > date,SentimentScore.date < tomorrow,
                                                                                     SentimentScore.input_data == input_data_id).count()

    count_yesterday, rel_hype_yesterday, abs_hype_yesterday = get_yesterday_data(date, input_data_id)

    if (sum_positive.sum is not None) and (sum_negative.sum is not None) and (sum_mixed.sum is not None) and (
            sum_neutral.sum is not None):
        absolute_hype = sum_positive.sum + sum_mixed.sum - sum_negative.sum
        relative_hype = (sum_positive.sum + sum_mixed.sum) / sum_negative.sum

        delta_count = 100*(count_today - count_yesterday)/count_yesterday
        delta_rel_hype = 100*(absolute_hype - abs_hype_yesterday)/abs_hype_yesterday
        delta_abs_hype = 100*(relative_hype - rel_hype_yesterday)/rel_hype_yesterday

        hype_record = SentimentHypeScore(
            input_data=input_data_id,
            absolute_hype=absolute_hype,
            absolute_hype_24delta=delta_abs_hype,
            relative_hype=relative_hype,
            relative_hype_24delta=delta_rel_hype,
            count=count_today,
            count_24delta=delta_count,
            date=date
        )
        existing = db.session.query(SentimentHypeScore).filter_by(input_data=input_data_id, date=date).first()
        if existing is None:
            db.session.add(hype_record)
        else:
            existing.input_data = input_data_id
            existing.absolute_hype = absolute_hype
            existing.absolute_hype_24delta = delta_abs_hype
            existing.relative_hype = relative_hype
            existing.relative_hype_24delta = delta_rel_hype
            existing.count = count_today
            existing.count_24delta = delta_count
            existing.date = date
        logger.info("Added hype score for {} and {}".format(input_data_id, date))
        db.session.commit()


def hype_score_for_coin(name, date):
    input_data = InputData.query.filter_by(name=name).one()
    if input_data is not None:
        calculate_hype_score(date=date, input_data_id=input_data)


def hype_score_for_all_coins(date):
    input_data_ids = db.session.query(SentimentScore.input_data.distinct()).all()
    for data_id in input_data_ids:
        calculate_hype_score(date, input_data_id=data_id[0])

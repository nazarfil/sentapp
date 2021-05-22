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
    logger.info("Recalculating hype score for {}".format(input_data_id))
    tomorrow = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)

    count_today, sum_mixed, sum_negative, sum_neutral, sum_positive = get_score_today_sum(date, input_data_id, tomorrow)
    count_yesterday, rel_hype_yesterday, abs_hype_yesterday = get_yesterday_data(date, input_data_id)

    absolute_hype = sum_positive + sum_mixed - sum_negative
    relative_hype = (sum_positive + sum_mixed) / sum_negative

    delta_count = 100 * (count_today - count_yesterday) / count_yesterday
    delta_rel_hype = 100 * (absolute_hype - abs_hype_yesterday) / abs_hype_yesterday
    delta_abs_hype = 100 * (relative_hype - rel_hype_yesterday) / rel_hype_yesterday

    create_or_updatehype_score_record(absolute_hype, count_today, date, delta_abs_hype, delta_count, delta_rel_hype,
                                      input_data_id, relative_hype)


def create_or_updatehype_score_record(absolute_hype, count_today, date, delta_abs_hype, delta_count, delta_rel_hype,
                                      input_data_id, relative_hype):
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
    try:
        existing = db.session.query(SentimentHypeScore).filter_by(input_data=input_data_id, date=date).first()
        existing.input_data = input_data_id
        existing.absolute_hype = absolute_hype
        existing.absolute_hype_24delta = delta_abs_hype
        existing.relative_hype = relative_hype
        existing.relative_hype_24delta = delta_rel_hype
        existing.count = count_today
        existing.count_24delta = delta_count
        existing.date = date
        db.session.commit()
    except:
        db.session.add(hype_record)
        db.session.commit()
    finally:
        logger.info("Added hype score for {} and {}".format(input_data_id, date))


def get_score_today_sum(date, input_data_id, tomorrow):
    try:
        sum_positive = db.session.query(func.sum(SentimentScore.positive).label('sum')).filter(
            SentimentScore.date > date,
            SentimentScore.date < tomorrow,
            SentimentScore.input_data == input_data_id).one()
        sum_negative = db.session.query(func.sum(SentimentScore.negative).label('sum')).filter(
            SentimentScore.date > date,
            SentimentScore.date < tomorrow,
            SentimentScore.input_data == input_data_id).one()
        sum_neutral = db.session.query(func.sum(SentimentScore.neutral).label('sum')).filter(SentimentScore.date > date,
                                                                                             SentimentScore.date < tomorrow,
                                                                                             SentimentScore.input_data == input_data_id).one()
        sum_mixed = db.session.query(func.sum(SentimentScore.mixed).label('sum')).filter(SentimentScore.date > date,
                                                                                         SentimentScore.date < tomorrow,
                                                                                         SentimentScore.input_data == input_data_id).one()
        count_today = db.session.query(SentimentScore).filter(SentimentScore.date > date,
                                                              SentimentScore.date < tomorrow,
                                                              SentimentScore.input_data == input_data_id).count()
        return count_today, sum_mixed.sum, sum_negative.sum, sum_neutral.sum, sum_positive.sum
    except Exception as e:
        logger.error(e)
        return 0, 0.0, 0.0, 0.0


def hype_score_for_coin(name, date):
    input_data = InputData.query.filter_by(name=name).one()
    if input_data is not None:
        calculate_hype_score(date=date, input_data_id=input_data.id)


def hype_score_for_all_coins(date):
    input_data_ids = db.session.query(SentimentScore.input_data.distinct()).all()
    for data_id in input_data_ids:
        calculate_hype_score(date, input_data_id=data_id[0])

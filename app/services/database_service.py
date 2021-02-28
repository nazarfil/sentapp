from app.models import *
from sqlalchemy.sql import func


def query_input_data_paged(page, offset):
    return InputData.query.paginate(page, offset, False).items


def query_input_data(name):
    InputData.query.filter_by(name=name).first()


def query_scraped_data_batch(input_data, batch_size):
    ScrapedData.query.filter_by(input_data=input_data.id).limit(batch_size).all()


def query_join_input_and_sentiment_by_name(name):
    return db.session.query(InputData, SentimentScore).join(SentimentScore).filter(
        InputData.name == name).all()


def query_sentiment_mean_score_for_coin(name):
    return db.session.query(InputData, SentimentMeanScore).join(SentimentMeanScore).filter(
        InputData.name == name).all()


def query_table_view():
    return TableView.query.filter(TableView.relative_hype != None).all()


def create_view_statement(db_instance):
    subq1 = db_instance.session.query(SentimentHypeScore.input_data.label("input_id"),
                                      func.max(SentimentHypeScore.date).label("max_date")).group_by(
        SentimentHypeScore.input_data).subquery()
    q2 = db_instance.session.query(
        SentimentHypeScore.relative_hype,
        SentimentHypeScore.absolute_hype,
        SentimentHypeScore.delta_tweets,
        SentimentHypeScore.date,
        SentimentHypeScore.input_data) \
        .select_from(SentimentHypeScore.__table__.
                     join(subq1, (SentimentHypeScore.date == subq1.c.max_date) & (
            SentimentHypeScore.input_data == subq1.c.input_id))) \
        .subquery()
    return db_instance.select([q2, InputData.price, InputData.ticker, InputData.name, InputData.market_cap]).where(
        InputData.id == q2.c.input_data)

from datetime import time
from multiprocessing import Process

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from app.log import setup_default_logger
from app.utility.paint import draw_graphs
from app.database.view import TableView
from app.database.models import *
import app.log as log

logger = log.def_logger


def create_and_save_scrape_data(input_data, source, text_data, tweet):
    scraped_data = TwitterData(text=text_data,
                               date=tweet["created_at"],
                               source=source,
                               input_data=input_data.id)
    db.session.add(scraped_data)
    db.session.commit()


def query_input_data_paged():
    return InputData.query.all()


def query_input_data(name):
    coin = InputData.query.filter_by(name=name).first()
    table_data = db.session.query(TableView).filter(TableView.name == coin.name).first()
    return {"coin": coin.serialized, "table_data": table_data.serialized}


def query_scraped_data_batch(input_data, batch_size):
    TwitterData.query.filter_by(input_data=input_data.id).limit(batch_size).all()


def query_join_input_and_sentiment_by_name(name):
    return db.session.query(InputData, SentimentScore).join(SentimentScore).filter(
        InputData.name == name).all()


def query_table_view(date):
    last_date = db.session.query(func.max(TableView.date)).one()
    return db.session.query(TableView).filter(TableView.relative_hype is not None, TableView.date == last_date).all()


def get_min_max_score():
    max_abs = db.session.query(TableView).order_by(TableView.absolute_hype.desc()).limit(5).all()
    min_abs = db.session.query(TableView).order_by(TableView.absolute_hype.asc()).first()
    max_rel = db.session.query(TableView).order_by(TableView.relative_hype.desc()).first()
    min_rel = db.session.query(TableView).order_by(TableView.relative_hype.asc()).first()
    max_count = db.session.query(TableView).order_by(TableView.count.desc()).first()
    min_count = db.session.query(TableView).order_by(TableView.count.asc()).first()
    return {
        "max_absolute_hype": max_abs[0].serialized,
        "min_absolute_hype": (min_abs.serialized),
        "max_relative_hype": (max_rel.serialized),
        "min_relative_hype": (min_rel.serialized),
        "max_count": (max_count.serialized),
        "min_count": (min_count.serialized),
        "top5_hype": [ma.serialized for ma in max_abs]
    }


def get_history_score(name, start_date, end_date, graph_types):
    types = graph_types.split(",")
    available_type = ["absolute_hype", "relative_hype", "count"]
    coin = InputData.query.filter(InputData.name == name).first()
    scores = []
    result = {
        'coin': coin.serialized
    }
    if coin is not None:
        scores = SentimentHypeScore.query.filter(SentimentHypeScore.date.between(start_date, end_date),
                                                 SentimentHypeScore.input_data == coin.id).order_by(
            SentimentHypeScore.date.asc()).all()

    for graph_type in types:
        if graph_type in available_type:
            result[graph_type] = []

    if len(scores) > 0:
        for score in scores:
            for graph_type in types:
                if graph_type in available_type:
                    point = [score.serialized['date'], score.serialized[graph_type]]
                    result[graph_type].append(point)

    return result


def get_long_scores():
    # input_data_ids = db.session.query(SentimentHypeScore.input_data).filter(and_(SentimentHypeScore.date=='2021-03-03',or_(SentimentHypeScore.absolute_hype>6, SentimentHypeScore.absolute_hype<-6))).all()
    input_data_ids = db.session.query(SentimentHypeScore.input_data).all()
    all_scores = {}
    for data_id in input_data_ids:
        name = db.session.query(InputData.name).filter_by(id=data_id).first()
        scores = db.session.query(SentimentHypeScore).filter_by(input_data=data_id).order_by(
            SentimentHypeScore.date.asc()).all()
        all_scores[name[0]] = [score.serialized for score in scores]
    p = Process(target=draw_graphs, args=(all_scores, "relative_hype",))
    p2 = Process(target=draw_graphs, args=(all_scores, "absolute_hype",))
    p.start()
    p.join()
    p2.start()
    p2.join()
    return all_scores


def create_financial_record(price=None, market_cap=None, the_date=None, volume=None, input_data=None):
    try:
        existing = db.session.query(FinancialData).filter_by(input_data=input_data, date=the_date).one()
        existing.price = price
        existing.volume = volume
        existing.market_cap = market_cap
        db.session.commit()
    except NoResultFound:
        record = FinancialData(price=price,
                               market_cap=market_cap,
                               date=the_date,
                               volume=volume,
                               input_data=input_data)
        db.session.add(record)
        db.session.commit()





def get_best_tweets(name, date):
    tweets = []
    tomorrow = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
    coin = db.session.query(InputData).filter_by(name=name).one()
    print("started query", datetime.now())
    best_tweets = db.session.query(TwitterData.source_id, TwitterData.followers) \
        .filter(TwitterData.followers != None).filter(TwitterData.input_data == coin.id, TwitterData.date > date,
                                                      TwitterData.date < tomorrow).order_by(
        TwitterData.followers.desc()).limit(5).all()

    try:
        for tweet in best_tweets:
            tweet_metric = {
                "twitter_id": tweet[0],
                "followers": tweet[1]
            }
            tweets.append(tweet_metric)
    except:
        log.error("Not such coin")
    return tweets


def get_top_6():
    subq_rank = db.session(
        SentimentHypeScore,
        func.rank().over(
            order_by=SentimentHypeScore.absolute_hype.desc(),
            partition_by=SentimentHypeScore.date).label('RANK')
    ).subquery.all()
    top_sentiments = query = db.session.query(subq_rank).filter(subq_rank.rank < 6)


"""
select ranked_scores.date,ranked_scores.input_data, ranked_scores.rank, ranked_scores.absolute_hype from
(SELECT sentiment_hype_score.*,
  rank() OVER (PARTITION BY date ORDER BY absolute_hype DESC)
  FROM sentiment_hype_score) ranked_scores  where rank <=6
"""

from multiprocessing import Process

from app.utility.paint import draw_graphs
from app.database.view import TableView
from app.database.models import *


def create_and_save_scrape_data(input_data, source, text_data, tweet):
    scraped_data = ScrapedData(text=text_data,
                               date=tweet["created_at"],
                               source=source,
                               input_data=input_data.id)
    db.session.add(scraped_data)
    db.session.commit()


def query_input_data_paged(page, offset):
    return InputData.query.paginate(page, offset, False).items


def query_input_data(name):
    InputData.query.filter_by(name=name).first()


def query_scraped_data_batch(input_data, batch_size):
    ScrapedData.query.filter_by(input_data=input_data.id).limit(batch_size).all()


def query_join_input_and_sentiment_by_name(name):
    return db.session.query(InputData, SentimentScore).join(SentimentScore).filter(
        InputData.name == name).all()


def query_table_view():
    return db.session.query(TableView).filter(TableView.relative_hype is not None).all()


def get_history_score(name, start_date, end_date, graph_types):
    types = graph_types.split(",")
    available_type = ["absolute_hype", "relative_hype", "tweets_count"]
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
    record = FinancialData(price=price,
                           market_cap=market_cap,
                           date=the_date,
                           volume=volume,
                           input_data=input_data)
    db.session.add(record)
    db.session.commit()

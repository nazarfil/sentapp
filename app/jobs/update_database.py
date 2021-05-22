from datetime import datetime

from app.database.models import SentimentHypeScore, SentimentScore, db, InputData, RedditMetrics
from sqlalchemy import and_, func

from app.database.view import TableView
from app.scraper.coingecko.cg_service import CgService
from app.scraper.messari.messari_scraper import get_messari_description
from app.scraper.reddit.reddit_client import RedditClient
from app.utility.formats import foramt_Y_M_D

cg = CgService()


def update_score_count():
    sentiments = SentimentHypeScore.query.all()
    for sentiment in sentiments:
        sentiment.count = db.session.query(func.count(SentimentScore.id)).filter(
            SentimentScore.date == sentiment.date).filter(SentimentScore.input_data == sentiment.input_data).first()
        print(sentiment.count)

    db.session.commit()


def update_string_id():
    coins = InputData.query.all()
    for coin in coins:
        name = coin.name
        string_id = cg.find_id(name)
        if string_id is not None:
            coin.string_id = string_id
        else:
            coin.string_id = name
    db.session.commit()


def update_description_of_coins():
    coins = InputData.query.all()
    for coin in coins:
        name = coin.name
        desc = get_messari_description(name)
        coin.description = desc
    db.session.commit()


def update_description_of_coin(coin, name):
    coin = InputData.query.filter_by(name=coin).one()
    desc = get_messari_description(name)
    coin.description = desc
    db.session.commit()


def update_order():
    today = datetime.today().date().strftime(foramt_Y_M_D)
    today_order = db.session.query(TableView).filter(TableView.date==today)\
        .order_by(TableView.absolute_hype.desc()).all()
    old_order = db.session.query(TableView).filter(TableView.date!=today)\
        .order_by(TableView.absolute_hype.desc()).all()
    cmc = db.session.query(TableView).order_by(TableView.market_cap.desc()).all()
    coins = InputData.query.all()
    table_dict = {}
    for i, table in enumerate(today_order):
        table_dict[table.name] = {"order": i + 1}

    for i, table in enumerate(old_order):
        table_dict[table.name] = {"order": i + 1 +len(today_order)}

    for i, table in enumerate(cmc):
        table_dict[table.name]["mc"] = i + 1

    for coin in coins:
        if coin.name in table_dict:
            coin.market_cap_id = table_dict[coin.name]["mc"]
            coin.order = table_dict[coin.name]["order"]
        else:
            coin.market_cap_id = len(coins)
            coin.order = len(coins)
    db.session.commit()


def update_old_scores():
    coins = InputData.query.all()
    end_date = '2021-04-17'
    for coin in coins:
        scores = db.session.query(SentimentHypeScore).filter(SentimentHypeScore.date <= end_date,
                                                             SentimentHypeScore.input_data == coin.id).all()
        avg = db.session.query(func.avg(SentimentHypeScore.absolute_hype).label('avg_abs'),
                               func.avg(SentimentHypeScore.count).label('avg_count')).filter(
            SentimentHypeScore.date > end_date, SentimentHypeScore.input_data == coin.id).one()
        for score in scores:
            score.absolute_hype = score.absolute_hype + abs(avg.avg_abs)
            score.count = score.count + avg.avg_count
            db.session.commit()


def update_reddit_url():
    coins = InputData.query.all()
    for coin in coins:
        lower_name = coin.name.lower()
        coin.reddit_url = lower_name
        db.session.commit()


def update_reddit_count():
    coins = InputData.query.all()
    reddit = RedditClient()
    today = datetime.today().date().strftime(foramt_Y_M_D)
    for coin in coins:
        subs = reddit.get_profile(coin.reddit_url)
        if subs != 0:
            try:
                existing = db.session.query(RedditMetrics).filter(RedditMetrics.input_data==coin.id, RedditMetrics.date==today).one()
                existing.subscribers=subs
            except:
                record = RedditMetrics(input_data=coin.id, subscribers=subs, date=today)
                db.session.add(record)
            db.session.commit()

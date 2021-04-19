from app.database.models import SentimentHypeScore, SentimentScore, db, InputData
from sqlalchemy import and_, func

from app.scraper.coingecko.cg_service import CgService
from app.scraper.messari.messari_scraper import get_messari_description

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
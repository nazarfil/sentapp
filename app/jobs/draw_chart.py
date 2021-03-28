
from app.database.models import db, InputData, SentimentHypeScore
from app.utility.paint import draw_sparkline


def draw_sparklines():
    coins = db.session.query(InputData).all()
    for coin in coins:
        last_scores = db.session.query(SentimentHypeScore).filter(SentimentHypeScore.input_data == coin.id).order_by(SentimentHypeScore.date.desc()).limit(7).all()
        if last_scores is not None and len(last_scores) > 1:
            items = [score.count for score in last_scores]
            draw_sparkline(items, coin.string_id)

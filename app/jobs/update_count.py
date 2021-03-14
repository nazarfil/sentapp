from app.database.models import SentimentHypeScore, SentimentScore, db
from sqlalchemy import and_, func


def update_score_count():
    sentiments = SentimentHypeScore.query.all()
    for sentiment in sentiments:
        sentiment.count = db.session.query(func.count(SentimentScore.id)).filter(
            SentimentScore.date == sentiment.date).filter(SentimentScore.input_data == sentiment.input_data).first()
        print(sentiment.count)

    db.session.commit()

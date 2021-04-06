from app import log

from app.algos.sentiment_aws import AwsClient
from app.database.models import db, InputData, ScrapedData, SentimentScore
import app.services.database_service as db_service

BATCH_SIZE = 100
logger = log.setup_custom_logger('services')

def assign_score(input_data, date, sentiment, source):
    sentiment_record = SentimentScore(
        input_data=input_data.id,
        sentiment=sentiment["Sentiment"],
        positive=sentiment["SentimentScore"]["Positive"],
        negative=sentiment["SentimentScore"]["Negative"],
        neutral=sentiment["SentimentScore"]["Neutral"],
        mixed=sentiment["SentimentScore"]["Mixed"],
        date=date,
        source=source

    )
    db.session.add(sentiment_record)
    db.session.commit()


def calculate_sentiment():
    logger.info("CALCULATING SENTIMENTS")
    name = "Cardano"
    input_data = db_service.query_input_data(name)
    data_remains = True
    client = AwsClient()
    while data_remains:
        scraped_data_list = db_service.query_scraped_data_batch(input_data, BATCH_SIZE)
        data_remains = len(scraped_data_list) > 0
        for data_record in scraped_data_list:
            sentiment = client.get_sentiment(text=data_record.text)
            assign_score(input_data, data_record.date, sentiment, AwsClient.name)
            db.session.delete(data_record)
            # commit (or flush)
            db.session.commit()


def calculate_sentiment_for_tweet(coin, tweet, client=AwsClient()):
    sentiment = client.get_sentiment(text=tweet.text)
    assign_score(coin, tweet.date, sentiment, client.name)

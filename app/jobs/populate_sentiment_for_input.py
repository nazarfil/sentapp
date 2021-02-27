from app.algos.sentiment_aws import AwsClient
from app.models import db, InputData, ScrapedData, SentimentScore

BATCH_SIZE = 100


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
    print("CALCULATING SENTIMENTS")
    input_data = InputData.query.filter_by(name="Cardano").first()
    data_remains = True
    client = AwsClient()
    while data_remains:
        scraped_data_list = ScrapedData.query.filter_by(input_data=input_data.id).limit(BATCH_SIZE).all()
        data_remains = len(scraped_data_list) > 0
        for data_record in scraped_data_list:
            sentiment = client.get_sentiment(text=data_record.text)
            print(sentiment)
            assign_score(input_data, data_record.date, sentiment, AwsClient.name)
            db.session.delete(data_record)
            # commit (or flush)
            db.session.commit()

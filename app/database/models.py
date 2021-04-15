from flask_sqlalchemy import SQLAlchemy
from datetime import timezone, datetime, timedelta

db = SQLAlchemy()


class InputData(db.Model):
    __tablename__ = 'input_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    source = db.Column(db.String(50))
    date = db.Column(db.Date)
    ticker = db.Column(db.String(32))
    order = db.Column(db.Integer)
    string_id = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(InputData, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<InputData {}>'.format(self.name)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.string_id,
                    name=self.name,
                    date=self.date,
                    source=self.source,
                    ticker=self.ticker,
                    order=self.order
                    )


class FinancialData(db.Model):
    __tablename__ = 'financial_data'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    price = db.Column(db.Numeric)
    market_cap = db.Column(db.Numeric)
    date = db.Column(db.Date)
    volume = db.Column(db.Numeric)

    def __init__(self, **kwargs):
        super(FinancialData, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<FinancialData {}>'.format(self.text)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.id,
                    volume=self.volume,
                    date=self.date,
                    price=self.price,
                    market_cap=self.market_cap,
                    input_data=self.input_data)


class ScrapedData(db.Model):
    __tablename__ = 'scraped_data'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(260))
    date = db.Column(db.DateTime)
    source = db.Column(db.String(60))
    source_id = db.Column(db.String(60))
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))

    def __init__(self, **kwargs) -> object:
        super(ScrapedData, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<ScrapedData {}>'.format(self.text)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.id, text=self.text, date=self.date, source=self.source, source_id=self.source_id,
                    input_data=self.input_data)


class TwitterDataMetric(db.Model):
    __tablename__ = 'twitter_data_metrics'
    id = db.Column(db.Integer, primary_key=True)
    scraped_data = db.Column(db.Integer, db.ForeignKey('scraped_data.id'))
    followers = db.Column(db.Integer)
    retweet = db.Column(db.Integer)
    replies = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    quotes = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(TwitterDataMetric, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<TwitterDataMetric {}>'.format(self.followers)

    @property
    def serialized(self):
        return dict(followers=self.followers,
                    retweet=self.retweet,
                    replies=self.replies,
                    likes=self.likes,
                    quotes=self.quotes)


class SentimentScore(db.Model):
    __tablename__ = 'sentiment_score'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    sentiment = db.Column(db.String(32))
    positive = db.Column(db.Numeric)
    negative = db.Column(db.Numeric)
    neutral = db.Column(db.Numeric)
    mixed = db.Column(db.Numeric)
    date = db.Column(db.DateTime)
    source = db.Column(db.String(60))

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.id, input_data=self.input_data, sentiment=self.sentiment,
                    positive=float(self.positive),
                    negative=float(self.negative),
                    neutral=float(self.neutral),
                    mixed=float(self.mixed),
                    date=self.date,
                    source=self.source)

    def __repr__(self):
        return '<SentimentScore {}>'.format(self.sentiment)


class SentimentHypeScore(db.Model):
    __tablename__ = 'sentiment_hype_score'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    absolute_hype = db.Column(db.Numeric)
    absolute_hype_24delta = db.Column(db.Numeric)
    relative_hype = db.Column(db.Numeric)
    relative_hype_24delta = db.Column(db.Numeric)
    count = db.Column(db.Integer)
    count_24delta = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, **kwargs):
        super(SentimentHypeScore, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<SentimentHypeScore {}>'.format(self.relative_hype)

    @property
    def serialized(self):
        return dict(id=self.id,
                    input_data=self.input_data,
                    absolute_hype=float(self.absolute_hype),
                    relative_hype=float(self.relative_hype),
                    count=float(self.count),
                    date=self.date_to_timestamp(self.date))

    @staticmethod
    def date_to_timestamp(dt):
        return (dt - datetime(1970, 1, 1, tzinfo=timezone.utc).date()) / timedelta(milliseconds=1)

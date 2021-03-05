from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from sqlalchemy.sql import func


class InputData(db.Model):
    __tablename__ = 'input_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    source = db.Column(db.String(50))
    date = db.Column(db.Date)
    ticker = db.Column(db.String(32))
    order = db.Column(db.Integer)
    price = db.Column(db.String(32))
    market_cap = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(InputData, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<InputData {}>'.format(self.name)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.id,
                    name=self.name,
                    date=self.date,
                    source=self.source,
                    ticker=self.ticker,
                    order=self.order,
                    price = self.price,
                    market_cap= self.market_cap
                    )

class ScrapedData(db.Model):
    __tablename__ = 'scraped_data'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(260))
    date = db.Column(db.Date)
    source = db.Column(db.String(60))
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))

    def __init__(self, **kwargs):
        super(ScrapedData, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<ScrapedData {}>'.format(self.text)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.id, text=self.text, date=self.date, source=self.source, input_data=self.input_data)


class SentimentScore(db.Model):
    __tablename__ = 'sentiment_score'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    sentiment = db.Column(db.String(32))
    positive = db.Column(db.Numeric)
    negative = db.Column(db.Numeric)
    neutral = db.Column(db.Numeric)
    mixed = db.Column(db.Numeric)
    date = db.Column(db.Date)
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


class SentimentMeanScore(db.Model):
    __tablename__ = 'sentiment_mean_score'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    sentiment = db.Column(db.String(32))
    positive = db.Column(db.Numeric)
    negative = db.Column(db.Numeric)
    neutral = db.Column(db.Numeric)
    mixed = db.Column(db.Numeric)
    date = db.Column(db.Date)
    source = db.Column(db.String(60))

    def __init__(self, **kwargs):
        super(SentimentMeanScore, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<SentimentMeanScore {}>'.format(self.sentiment)

    @property
    def serialized(self):
        return dict(id=self.id,
                    input_data=self.input_data,
                    sentiment=self.sentiment,
                    positive=float(self.positive),
                    negative=float(self.negative),
                    neutral=float(self.neutral),
                    mixed=float(self.mixed),
                    date=self.date,
                    source=self.source)


class SentimentSumScore(db.Model):
    __tablename__ = 'sentiment_sum_score'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    sentiment = db.Column(db.String(32))
    positive = db.Column(db.Numeric)
    negative = db.Column(db.Numeric)
    neutral = db.Column(db.Numeric)
    mixed = db.Column(db.Numeric)
    date = db.Column(db.Date)
    source = db.Column(db.String(60))

    def __init__(self, **kwargs):
        super(SentimentSumScore, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<SentimentSumScore {}>'.format(self.sentiment)

    @property
    def serialized(self):
        return dict(id=self.id,
                    input_data=self.input_data,
                    sentiment=self.sentiment,
                    positive=float(self.positive),
                    negative=float(self.negative),
                    neutral=float(self.neutral),
                    mixed=float(self.mixed),
                    date=self.date,
                    source=self.source)

class SentimentHypeScore(db.Model):
    __tablename__ = 'sentiment_hype_score'
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Integer, db.ForeignKey('input_data.id'))
    absolute_hype = db.Column(db.Numeric, )
    relative_hype = db.Column(db.Numeric)
    delta_tweets = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, **kwargs):
        super(SentimentHypeScore, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<SentimentHypeScore {}>'.format(self.sentiment)

    @property
    def serialized(self):
        return dict(id=self.id,
                    input_data=self.input_data,
                    absolute_hype=self.absolute_hype,
                    positive=float(self.positive),
                    relative_hype=float(self.relative_hype),
                    delta_tweets=float(self.delta_tweets),
                    date=self.date)


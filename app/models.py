from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InputData(db.Model):
    __tablename__ = 'input_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    source = db.Column(db.String(50))
    date = db.Column(db.Date)
    ticker = db.Column(db.String(32))
    order = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(InputData, self).__init__(**kwargs)
        # do custom stuff

    def __repr__(self):
        return '<InputData {}>'.format(self.name)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return dict(id=self.id, name=self.name, date=self.date, source=self.source, ticker=self.ticker, order=self.order)

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
        return dict(id=self.id, input_data=self.input_data, sentiment=self.sentiment, positive=self.positive,
                    negative=self.negative, neutral=self.negative, mixed=self.negative, date=self.date,
                    source=self.source)

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
        return dict(id=self.id, input_data=self.input_data, sentiment=self.sentiment, positive=self.positive,
                    negative=self.negative, neutral=self.negative, mixed=self.negative, date=self.date,
                    source=self.source)

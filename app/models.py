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


class SentimentMeanScore(db.Model):
    __tablename__ = 'sentiment__mean_score'
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

# attaches the view to the metadata using the select statement
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric, String, Date

from app.database.models import SentimentHypeScore, InputData, FinancialData

from sqlalchemy.sql import func

Base = declarative_base()


class TableView(Base):
    __tablename__ = 'table_view'
    name = Column(String(32), primary_key=True)
    ticker = Column(String(32))
    market_cap = Column(String(32))
    price = Column(String(32))
    order = Column(String(32))
    absolute_hype = Column(Numeric)
    absolute_hype_24delta = Column(Numeric)
    relative_hype = Column(Numeric)
    relative_hype_24delta = Column(Numeric)
    count = Column(Numeric)
    count_24delta = Column(Numeric)
    date = Column(Date)

    @property
    def serialized(self):
        return dict(
            name=self.name,
            order=self.order,
            ticker=self.ticker,
            price=float(self.get_price()),
            market_cap=float(self.get_market_cap()),
            absolute_hype=float(self.get_abs_hyp()),
            absolute_hype_24delta=float(self.get_abs24()),
            relative_hype=float(self.get_rel_hyp()),
            relative_hype_24delta=float(self.get_rel4()),
            count=float(self.get_count()),
            count_24delta=float(self.get_count24()),
            date=self.date)

    def get_rel_hyp(self):
        if self.relative_hype is None:
            return 0
        else:
            return self.relative_hype

    def get_abs_hyp(self):
        if self.absolute_hype is None:
            return 0
        else:
            return self.absolute_hype

    def get_count(self):
        if self.count is None:
            return 0
        else:
            return self.count

    def get_price(self):
        if self.price is None:
            return 0
        else:
            return self.price

    def get_market_cap(self):
        if self.market_cap is None:
            return 0
        else:
            return self.market_cap

    def get_abs24(self):
        if self.absolute_hype_24delta is None:
            return 0
        else:
            return self.absolute_hype_24delta

    def get_rel4(self):
        if self.relative_hype_24delta is None:
            return 0
        else:
            return self.relative_hype_24delta

    def get_count24(self):
        if self.count_24delta is None:
            return 0
        else:
            return self.count_24delta


def create_view_statement(db_instance):
    max_date = db_instance.session \
        .query(SentimentHypeScore.input_data.label("input_id"), func.max(SentimentHypeScore.date).label("max_date")) \
        .group_by(SentimentHypeScore.input_data) \
        .subquery()

    find_data = db_instance.session.query(FinancialData.input_data.label("in_id"), FinancialData.price,
                                          FinancialData.volume, FinancialData.market_cap) \
        .select_from(FinancialData.__table__.join(max_date, (FinancialData.date == max_date.c.max_date) & (
            FinancialData.input_data == max_date.c.input_id))) \
        .subquery()

    hype_score = db_instance.session \
        .query(SentimentHypeScore.relative_hype, SentimentHypeScore.absolute_hype, SentimentHypeScore.count,
               SentimentHypeScore.date, SentimentHypeScore.input_data, SentimentHypeScore.absolute_hype_24delta,
               SentimentHypeScore.relative_hype_24delta, SentimentHypeScore.count_24delta, ) \
        .select_from(SentimentHypeScore.__table__.join(max_date, (SentimentHypeScore.date == max_date.c.max_date) & (
            SentimentHypeScore.input_data == max_date.c.input_id))) \
        .subquery()
    return db_instance.select([find_data, hype_score, InputData.ticker, InputData.name, InputData.order]) \
        .where(InputData.id == hype_score.c.input_data).where(find_data.c.in_id == hype_score.c.input_data)

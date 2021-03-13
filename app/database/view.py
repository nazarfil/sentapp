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
    #market_cap = Column(String(32))
    #price = Column(String(32))
    order = Column(String(32))
    absolute_hype = Column(Numeric)
    relative_hype = Column(Numeric)
    count = Column(Numeric)
    date = Column(Date)

    @property
    def serialized(self):
        return dict(
            name=self.name,
            order=self.order,
            ticker=self.ticker,
            #price=self.price,
            #market_cap=self.market_cap,
            absolute_hype=float(self.get_abs_hyp()),
            relative_hype=float(self.get_rel_hyp()),
            count=float(self.get_count()),
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


def create_view_statement(db_instance):
    subq1 = db_instance.session\
        .query(SentimentHypeScore.input_data.label("input_id"), func.max(SentimentHypeScore.date).label("max_date"))\
        .group_by(SentimentHypeScore.input_data)\
        .subquery()

    q2 = db_instance.session\
        .query(SentimentHypeScore.relative_hype, SentimentHypeScore.absolute_hype, SentimentHypeScore.count, SentimentHypeScore.date,  SentimentHypeScore.input_data) \
        .select_from(SentimentHypeScore.__table__.join(subq1, (SentimentHypeScore.date == subq1.c.max_date) & (SentimentHypeScore.input_data == subq1.c.input_id))) \
        .subquery()
    return db_instance.select([q2, InputData.ticker, InputData.name, InputData.order, FinancialData.price, FinancialData.market_cap])\
                        .where(InputData.id == q2.c.input_data)
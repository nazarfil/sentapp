# attaches the view to the metadata using the select statement
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric, String, Date

Base = declarative_base()


class TableView(Base):
    __tablename__ = 'table_view'
    name = Column(String(32), primary_key=True)
    ticker = Column(String(32))
    market_cap = Column(String(32))
    price = Column(String(32))
    order = Column(String(32))
    absolute_hype = Column(Numeric)
    relative_hype = Column(Numeric)
    tweets_count = Column(Numeric)
    date = Column(Date)

    @property
    def serialized(self):
        return dict(
            name=self.name,
            order=self.order,
            ticker=self.ticker,
            price=self.price,
            market_cap=self.market_cap,
            absolute_hype=float(self.get_abs_hyp()),
            relative_hype=float(self.get_rel_hyp()),
            tweets_count=float(self.get_count()),
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
        if self.tweets_count is None:
            return 0
        else:
            return self.tweets_count

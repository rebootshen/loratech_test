from . import db
import datetime
from marshmallow import fields, Schema
from sqlalchemy import text, desc


class PriceModel(db.Model):
    """
    Price Model
    """

    __tablename__ = 'imported_closes'

    ticker = db.Column(db.String(128), primary_key=True)
    day = db.Column(db.Date, primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, data):
        self.ticker = data.get('ticker')
        self.day = data.get('day')
        self.price = data.get('price')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_prices():
        return PriceModel.query.all()

    @staticmethod
    def get_one_price(id):
        return PriceModel.query.get(id)

    @staticmethod
    def get_prices_by_ticker(value):
        return PriceModel.query.filter_by(ticker=value)

    @staticmethod
    def get_prices_by_date(ticker, day, time_window):
        #return PriceModel.query.filter_by(ticker = ticker, day=day).limit(time_window)
        return PriceModel.query.filter(text("ticker=:ticker and day<=:day")).params(ticker=ticker, day=day).order_by(desc(text("day"))).limit(time_window)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class PriceSchema(Schema):
    """
    Price Schema
    """
    ticker = fields.Str(required=True)
    day = fields.Date(required=True)
    price = fields.Float(required=True)
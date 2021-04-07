from datetime import datetime, timezone, timedelta

from sqlalchemy.orm.exc import NoResultFound

from app import log
from app.database.models import InputData, SentimentHypeScore, db, FinancialData
from sqlalchemy import func, distinct

from app.scraper.cryptocompare import cc_service as cc
from app.scraper.coingecko.cg_service import CgService
from app.services.database_service import create_financial_record
from app.utility.formats import foramt_D_M_Y

cg = CgService()
logger = log.setup_custom_logger('services')


def populate_price_and_market_cap(start_id):
    coins = InputData.query.filter(InputData.id > start_id).order_by(InputData.id).all()
    dates = db.session.query(SentimentHypeScore.date).distinct().order_by(SentimentHypeScore.date.desc()).all()
    for coin in coins:
        coin_name = coin.name
        max_date = db.session.query(func.max(distinct(FinancialData.date))).filter(
            FinancialData.input_data == coin.id).first()
        if max_date[0] is not None:
            for date in dates:
                if date > max_date:
                    create_financial_data_for_date(coin, coin_name, date[0])


def create_financial_data_for_date(coin, coin_name, date):
    history = cg.get_coin_history(coin_name=coin_name, history_date=date.strftime(foramt_D_M_Y))
    if history is not None:
        logger.info("Filling in history for " + str(coin_name))
        try:
            price_day = history['market_data']['current_price']['usd']
            market_cap = history['market_data']['market_cap']['usd']
            volume = history['market_data']['total_volume']['usd']
            create_financial_record(price=price_day, market_cap=market_cap, the_date=date, volume=volume,
                                    input_data=coin.id)
        except:
            logger.error("Could not fill in history for " + str(coin_name))
    else:
        logger.error("Could not query history for " + str(coin_name))


def create_financial_record_for_coins(coins, date):
    coin_ids = ""
    for coin in coins:
        if coin.string_id is not None:
            coin_ids = coin_ids + coin.string_id + ","
    coin_ids = coin_ids[:-1]
    cg_prices = cg.get_price(coin_ids)
    for coin in coins:
        if coin.string_id in cg_prices.keys():
            data = cg_prices[coin.string_id]
            usd_price = data['usd']
            usd_market = data['usd_market_cap']
            usd_vol = data['usd_24h_vol']
            create_financial_record(usd_price, usd_market, date, usd_vol, coin.id)
        else:
            logger.warn("No CoingeckoId for : {}".format(coin.name))


def get_score_max_date():
    return db.session.query(func.max(distinct(SentimentHypeScore.date))).first()


def get_score_min_date():
    return db.session.query(func.min(distinct(SentimentHypeScore.date))).first()


def get_score_date_all_count():
    return db.session.query(func.count(distinct(SentimentHypeScore.date))).first()


def populate_prices_history():
    coins = InputData.query.all()
    dates_count = get_score_date_all_count()[0]
    max_date_res = get_score_max_date()[0]
    if max_date_res is not None:
        max_date = date_to_timestamp(max_date_res)
    for coin in coins:
        coin_name = coin.ticker
        historical_prices = cc.get_historical_data(coin=coin_name, limit=dates_count, to_date=max_date)
        print(historical_prices)
        if historical_prices['Response'] != 'Success':
            logger.error("Error calling ")
        else:
            for price in historical_prices['Data']['Data']:
                print(price)


def date_to_timestamp(dt):
    return (dt - datetime(1970, 1, 1, tzinfo=timezone.utc).date()) / timedelta(seconds=1)

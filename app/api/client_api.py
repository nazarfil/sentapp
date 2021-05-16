from os import environ

from flasgger import swag_from

import app.services.database_service as db_service
from app.services.sparkline_service import draw_sparklines
from app.utility.resources.data import data_demo
from flask import make_response
from datetime import datetime
from flask import (Blueprint)
from flask import jsonify
from app.utility.formats import foramt_Y_M_D
from flask import request

client_bp = Blueprint('/api', __name__, url_prefix='/api')
origin_prod = 'https://coin.sentimentcap.com'
origin_dev = '*'
origin = origin_dev
FLASK_ENV = environ.get('FLASK_ENV')
if FLASK_ENV is not None:
    if FLASK_ENV=="production":
        origin = origin_prod

# CLIENT API
@client_bp.route('coins', methods=['GET'])
@swag_from('/app/api/swagger/coins.yml')
def get_coins():
    list_of_coins = db_service.query_input_data_paged()
    response = make_response(jsonify({'data': [result.serialized for result in list_of_coins]}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@client_bp.route('coin/<name>', methods=['GET'])
@swag_from('/app/api/swagger/coin.yml')
def get_coins_by_name(name):
    coin = db_service.query_input_data(name)
    response = make_response(jsonify({'data': coin}))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@client_bp.route('healthcheck', methods=["GET"])
def healthcheck():
    return jsonify({
        'status': 'OK'
    })


@client_bp.route('table', methods=['GET'])
@swag_from('/app/api/swagger/table.yml')
def get_hype():
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    hypes = db_service.query_table_view(date)
    response = make_response(jsonify([hype.serialized for hype in hypes]))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@client_bp.route('table/demo', methods=["GET"])
@swag_from('/app/api/swagger/coins.yml')
def get_demo_table():
    response = make_response(jsonify(data_demo))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@client_bp.route('draw_bars')
@swag_from('/app/api/swagger/draw.yml')
def get_long_term_score():
    draw_sparklines()
    return jsonify({"ok": "ok"})


@client_bp.route('history/hype_score/<name>')
@swag_from('/app/api/swagger/history.yml')
def get_history_hype_score(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    start_date = request.args.get('start_date', default='2021-01-01', type=str)
    end_date = request.args.get('end_date', default=today, type=str)
    graph_types = request.args.get('graph', default='absolute_hype,count,relative_hype', type=str)
    history_scores = db_service.get_history_score(name, start_date, end_date, graph_types)
    response = make_response(jsonify(history_scores))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@client_bp.route('info/best_tweets/<name>')
@swag_from('/app/api/swagger/best_tweets.yml')
def get_best_tweets(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    best_tweets = db_service.get_best_tweets(name, date)
    response = make_response(jsonify({"best_tweets": best_tweets}))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response

@client_bp.route('info/top_scores')
def get_top_scores():
    top6 = db_service.get_top_6()
    response = make_response(jsonify({"top6": top6}))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response

@client_bp.route('global')
@swag_from('/app/api/swagger/global.yml')
def get_blobal():
    min_max = db_service.get_min_max_score()
    response = make_response(jsonify({"global": {"min_max": min_max}}))
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


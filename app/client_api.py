import app.services.database_service as db_service
from app.utility.data import data_demo
from flask import make_response
from datetime import datetime
from flask import (Blueprint)
from flask import jsonify
from app.utility.formats import foramt_Y_M_D
from flask import request


client_bp = Blueprint('/api', __name__, url_prefix='/api')

# CLIENT API
@client_bp.route('calculate_score', methods=['POST'])
def calculate_score():
    query = {"data": "not_suppeorted_yet"}
    return query


@client_bp.route('coins', methods=['GET'])
def get_coins():
    page = request.args.get('page', default=1, type=int)
    offset = request.args.get('offset', default=10, type=int)
    list_of_coins = db_service.query_input_data_paged(page, offset)
    return jsonify({
        'data': [result.serialized for result in list_of_coins]
    })


def create_result(input_data, score):
    return {
        "name": input_data.name,
        "score": score.sentiment,
        "date": score.date
    }


@client_bp.route('scores/<name>', methods=['GET'])
def get_scores(name):
    sentiment_scores = db_service.query_join_input_and_sentiment_by_name(name)
    return jsonify({
        'data': [create_result(input_data, score) for (input_data, score) in sentiment_scores]
    })


def create_mean_result(input_data, mean_score):
    return {
        "name": input_data.name,
        "score": mean_score.sentiment,
        "date": mean_score.date
    }


@client_bp.route('mean_scores/<name>', methods=['GET'])
def get_mean_scores(name):
    sentiment_scores = db_service.query_sentiment_mean_score_for_coin(name)
    return jsonify(
        {'data': [create_mean_result(input_data, mean_score) for (input_data, mean_score) in sentiment_scores]})

@client_bp.route('healthcheck', methods=["GET"])
def healthcheck():
    return jsonify({
        'status': 'OK'
    })


@client_bp.route('table', methods=['GET'])
def get_hype():
    hypes = db_service.query_table_view()
    response = make_response(jsonify([hype.serialized for hype in hypes]))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@client_bp.route('table/demo', methods=["GET"])
def get_demo_table():
    response = make_response(jsonify(data_demo))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@client_bp.route('try')
def get_long_term_score():
    scores = db_service.get_long_scores()
    return jsonify({"ok": "ok"})


@client_bp.route('history/hype_score/<name>')
def get_history_hype_score(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    start_date = request.args.get('start_date', default='2021-01-01', type=str)
    end_date = request.args.get('end_date', default=today, type=str)
    graph_types = request.args.get('graph',default='absolute_hype',type=str)
    history_scores = db_service.get_history_score(name, start_date, end_date,graph_types)
    response = make_response(jsonify(history_scores))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
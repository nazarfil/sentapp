import app.services.database_service as db_service
from app.jobs.draw_chart import draw_sparklines
from app.utility.paint import draw_sparkline
from app.utility.resources.data import data_demo
from flask import make_response
from datetime import datetime
from flask import (Blueprint)
from flask import jsonify
from app.utility.formats import foramt_Y_M_D
from flask import request

client_bp = Blueprint('/api', __name__, url_prefix='/api')


# CLIENT API
@client_bp.route('coins', methods=['GET'])
def get_coins():
    page = request.args.get('page', default=1, type=int)
    offset = request.args.get('offset', default=10, type=int)
    list_of_coins = db_service.query_input_data_paged(page, offset)
    return jsonify({
        'data': [result.serialized for result in list_of_coins]
    })


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


@client_bp.route('draw_bars')
def get_long_term_score():
    draw_sparklines()
    return jsonify({"ok": "ok"})


@client_bp.route('history/hype_score/<name>')
def get_history_hype_score(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    start_date = request.args.get('start_date', default='2021-01-01', type=str)
    end_date = request.args.get('end_date', default=today, type=str)
    graph_types = request.args.get('graph', default='absolute_hype,count,relative_hype', type=str)
    history_scores = db_service.get_history_score(name, start_date, end_date, graph_types)
    response = make_response(jsonify(history_scores))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@client_bp.route('global')
def get_blobal():
    min_max = db_service.get_min_max_score()
    return jsonify({
        "global": {
            "min_max": min_max
        }
    })

from flask import (Blueprint)
bp = Blueprint('/api', __name__, url_prefix='/api')

@bp.route('coins', methods=['GET'])
def index():
    query = "bitcoin or btc"
    return query



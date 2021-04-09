from sqlalchemy.orm.exc import NoResultFound

from app.database.models import db, InputData
from datetime import date

from app.scraper.coingecko.cg_service import CgService

cg = CgService()


def populate_db_api(row, source):
    today = date.today()
    try:
        existing = db.session.query(InputData).filter_by(name=row['name']).one()
        existing.order = row['id']
    except NoResultFound:
        new_input_data = InputData(order=row['id'], name=row['name'], ticker=row['ticker'],
                                   date=today, source=source)
        string_id = find_string_id(new_input_data.name)
        new_input_data.string_id = string_id
        db.session.add(new_input_data)

    db.session.commit()


def find_string_id(name):
    string_id = cg.find_id(name)
    if string_id is not None:
        return string_id
    else:
        return name


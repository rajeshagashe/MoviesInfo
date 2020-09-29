from flask import (
    Blueprint, request
)

from app.models.movies import MoviesData
from app.extensions import sql_db

import traceback
import datetime
import json

crud_blueprint = Blueprint('crud', __name__)

@crud_blueprint.route('/get/<int:record_id>', methods=["GET"])
@crud_blueprint.route('/get', methods=["GET"])
def read(record_id=0):
    try:
        if not record_id:
            row = MoviesData.query.all()
            response = list()
            for i in row:
                response.append(i.to_json())
            sql_db.session.commit()
            return json.dumps(response)
        else:
            row = MoviesData.query.get(record_id)

        return json.dumps([row.to_json()])
    except:
        traceback.print_exc()
        return "Something went wrong"
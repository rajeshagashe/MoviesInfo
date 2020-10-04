from flask import (
    Blueprint, request
)

from app.models.movies import MoviesData
from app.models.user import UserData
from app.extensions import sql_db
from app.views.api_decorators import authenticate_if_user, authorize_if_admin

import traceback
import datetime
import json
from sqlalchemy import func

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/movies", methods=["GET"])
@authenticate_if_user
def search():
    try:
        # consider saving movie names without spaces to allow searches without spaces
        params = dict(request.args)
        
        search_result = False

        if params.get("name"):
            name_query = "%" + params.get("name").replace(' ', '%') + "%" 
            search_result = MoviesData.query \
                .filter(func.lower(MoviesData.name) \
                .like(func.lower(name_query)))

        if params.get("director"):
            director_query = "%" + params.get("director").replace(' ', '%') + "%"
            if search_result:
                search_result = search_result \
                    .filter(func.lower(MoviesData.director) \
                    .like(func.lower(director_query)))
            else:
                search_result = MoviesData.query \
                    .filter(func.lower(MoviesData.director) \
                    .like(func.lower(director_query)))

        if not search_result:
            # all results returned if no search params provided.
            search_result = MoviesData.query 

        res = list()
        for each in search_result.all():
            # print(each.director, '\n')
            res.append(each.to_json()) 

        sql_db.session.commit()
        return json.dumps(res)

    except Exception as e:
        sql_db.session.rollback()
        return e.__str__()
from flask import (
    Blueprint, request
)

from app.models.movies import MoviesData
from app.extensions import sql_db
from app.views.api_decorators import authenticate_if_user, authorize_if_admin
# from app.views.search import get_user

import traceback
import datetime
import json

crud_blueprint = Blueprint("crud", __name__)

@crud_blueprint.route("/read/<int:record_id>", methods=["GET"])
@crud_blueprint.route("/read", methods=["GET"])
@authenticate_if_user
def read(record_id=0):
    try:
        if not record_id:
            row = MoviesData.query.all()
            response = list()
            for i in row:
                response.append(i.to_json())
            response.append({"status": "success", "msg": "crud/read msg"})
            return json.dumps(response)
        else:
            row = MoviesData.query.get(record_id)

        sql_db.session.commit()
        return json.dumps([row.to_json(), {"status": "success", "msg": "crud/read msg"}])

    except:
        sql_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"


@crud_blueprint.route("/create", methods=["POST"])
@authorize_if_admin
def create():
    try:
        entry = request.get_json()
        movie = MoviesData()

        if not check_if_all_fields(entry):
            # assumption all fields necessary.
            raise Exception("All fields not provided.")

        invalid_field_types = check_if_field_types_invalid(entry)
        if invalid_field_types:
            raise Exception("Invalid Field_types")

        movie.name = entry.get("name")
        movie.nn_popularity = entry.get("99popularity")
        movie.director = entry.get("director")
        movie.genre = ",".join(sorted([i.strip() for i in entry.get("genre")]))
        movie.imdb_score = entry.get("imdb_score")

        sql_db.session.add(movie)
        sql_db.session.commit()

        return json.dumps([movie.to_json(), {"status": "success", "msg": "New movie added."}])

    except Exception as e:
        sql_db.session.rollback()
        
        if e.__str__() == "All fields not provided.":
            return e.__str__() + "\n" + "fields required: \n\nname\n99_popularity\ndirector\ngenre\nimdb_score\n"
        if e.__str__() == "Invalid Field_types":
            return e.__str__() + "\n" + invalid_field_types
        
        traceback.print_exc()
        return "Something went wrong"

@crud_blueprint.route("/update", methods=["PATCH"])
@crud_blueprint.route("/update/<int:movie_id>", methods=["PATCH"])
@authorize_if_admin
def update(movie_id=None):
    try:
        if not movie_id:
            raise Exception("Movie ID not found")

        update = dict()
        update["updated_at"] = datetime.datetime.now()
        request_content = request.get_json()
        
        if request_content.get("99popularity"):
            update["nn_popularity"] = request_content.get("99popularity") 
            
        if request_content.get("name"):
            update["name"] = request_content.get("name") 
                
        if request_content.get("director"):
            update["director"] = request_content.get("director") 
                
        if request_content.get("genre"):
            update["genre"] = request_content.get("genre") 
                
        if request_content.get("imdb_score"):
            update["imdb_score"] = request_content.get("imdb_score")

        invalid_field_types = check_if_field_types_invalid(update)
        if invalid_field_types:
            raise Exception("Invalid Field_types")

        if update.get("genre"):
            update["genre"] = ",".join(sorted([i.strip() for i in update["genre"]]))

        target_row = MoviesData.query.filter_by(id=movie_id)
        target_row.update(update)
        sql_db.session.commit()
        
        update.pop("updated_at")
        return json.dumps([update, {"status": "success", "msg": "Changes Saved."}])

    except Exception as e:
        sql_db.session.rollback()
        
        if e.__str__() ==  "Movie ID not found":
            return e.__str__() + "\n" + "please provide id of the movie you want to edit."
        if e.__str__() ==  "Invalid Field_types":
            return e.__str__() + "\n" + invalid_field_types
        
        traceback.print_exc()
        return "Something went wrong."

@crud_blueprint.route('/delete', methods=["DELETE"])
@crud_blueprint.route('/delete/<int:movie_id>', methods=["DELETE"])
@authorize_if_admin
def delete(movie_id=None):
    try:
        if not movie_id:
            raise Exception("Movie ID not found")

        target_row = MoviesData.query.filter_by(id=movie_id)
        movie_details = target_row.first()
        if not movie_details:
            raise Exception("No record corresponding to the ID provided")
        target_row.delete()
        sql_db.session.commit()

        return json.dumps([movie_details.to_json(), {"status": "success", "msg": "Deleted."}])

    except Exception as e:
        sql_db.session.rollback()
        
        if e.__str__() ==  "Movie ID not found":
            return e.__str__() + "\n" + "please provide id of the movie you want to delete."    
        if e.__str__() ==  "No record corresponding to the ID provided":
            return e.__str__()

        traceback.print_exc()
        return "Something went wrong."



def check_if_all_fields(entry):
    name = entry.get("name") 
    nn_popularity = entry.get("99popularity")
    director = entry.get("director")
    genre = entry.get("genre")
    imdb_score = entry.get("imdb_score")

    if (name and nn_popularity and director and genre and imdb_score):
        return True

    print(name,nn_popularity,director,genre,imdb_score) 
    return False

def check_if_field_types_invalid(entry):
    name = entry.get("name", "") 
    nn_popularity = entry.get("99popularity", 0)
    director = entry.get("director", "")
    genre = entry.get("genre", [""])
    imdb_score = entry.get("imdb_score", 0)

    error_msg = ""

    if not(isinstance(name, (str))):
        error_msg += "name must be a string, \n"
    if not(isinstance(nn_popularity, (float, int))):
        error_msg += "nn_popularity must be a number, \n"
    if not(isinstance(director, (str))):
        error_msg += "director must be a string, \n"
    if not(isinstance(genre, (list))):
        error_msg += "genre must be a list of strings, \n"
    if isinstance(genre, (list)):
        for each in genre:
            if not(isinstance(each, (str))):
                error_msg += "genre must be a list of strings, \n"
                break
    if not(isinstance(imdb_score, (float, int))):
        error_msg += "imdb_score must be a number. \n"

    return error_msg
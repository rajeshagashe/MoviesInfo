from flask import (
    Blueprint, request, session, g
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import UserData
from app.extensions import sql_db
from app.views.api_decorators import authenticate_if_user, authorize_if_admin
from app.views.search import search_blueprint
from app.views.crud import crud_blueprint

import traceback
import datetime
import json
from sqlalchemy import func

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/register", methods=["POST"])
def register():
    try:
        form = request.get_json()
        user_name = str(form.get("user_name", ""))
        password = str(form.get("password",""))
        user_role = str(form.get("user_role", "user"))

        if not user_name:
            raise Exception("user_name required.")
        
        if not password:
            raise Exception("password required.")

        if str(user_role) not in ["user", "admin"]:
            raise Exception("Invalid user_role.")

        if check_if_user_exists(user_name):
            raise Exception("user_name taken.")
        
        user = UserData()
        user.user_name = user_name
        user.password = generate_password_hash(password)
        user.user_role = user_role

        sql_db.session.add(user)
        sql_db.session.commit()
        return json.dumps([user.to_json()])

    except Exception as e:
        sql_db.session.rollback()
        if e.__str__() in ["user_name required.", "password required.", \
            "Invalid user_role.", "user_name taken."]:
            return e.__str__()

        traceback.print_exc()
        return "Something went wrong."

@user_blueprint.route("/login", methods=["POST"])
def login():
    try:
        form = request.get_json()
        user_name = str(form.get("user_name"))
        password = str(form.get("password"))
        
        user = check_if_user_exists(user_name)

        if not user:
            raise Exception('Incorrect username.')
        elif not check_password_hash(user.password, password):
            raise Exception('Incorrect password.')

        session.clear()
        session['user_id'] = user.id

        sql_db.session.commit()
        return json.dumps([user.to_json()])

    except Exception as e:
        sql_db.session.rollback()
        if e.__str__() in ['Incorrect username.', 'Incorrect password.']:
            return e.__str__()
        traceback.print_exc()
        return "Something went wrong."

@user_blueprint.route("/logout", methods=["DELETE"])
def logout():
    try:
        session.clear()
        return json.dumps(["Logged Out."]) 
    except:
        return "Please Try Again."

@crud_blueprint.before_app_request
@search_blueprint.before_app_request
@user_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id', 0)

    if not user_id:
        g.user = None
    else:
        g.user = get_user(user_id)

def get_user(user_id):
    user = UserData.query.filter_by(id=user_id)
    user_count = user.count()
    if user_count:
        return user.first()
    return False

def check_if_user_exists(user_name):
    user = UserData.query.filter_by(user_name=user_name)
    user_count = user.count()
    if user_count:
        return user.first()
    return False
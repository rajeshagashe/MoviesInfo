from flask import request
from functools import wraps

def authenticate_if_user(func):
    @wraps(func)
    def wrap(**kwargs):
        if request.headers.get("user_id", False):
            res = func(**kwargs)
        else:
            res = "please log in to access movies info"

        return res

    return wrap

def authorize_if_admin(func):
    @wraps(func)
    def wrap(**kwargs):
        if request.headers.get("user_role", "") == "admin":
            res = func(**kwargs)
        else:
            res = "admin access required to perform this action."

        return res

    return wrap


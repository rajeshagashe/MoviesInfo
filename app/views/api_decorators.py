from flask import g
from functools import wraps

def authenticate_if_user(func):
    @wraps(func)
    def wrap(**kwargs):
        if g.user and g.user:            
            res = func(**kwargs)
        else:
            res = "please log in to access movies info"

        return res

    return wrap

def authorize_if_admin(func):
    @wraps(func)
    def wrap(**kwargs):
        if g.user and g.user.user_role == "admin":
            res = func(**kwargs)
        else:
            res = "admin access required to perform this action."

        return res

    return wrap


from app.extensions import sql_db
import datetime

class UserData(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    user_name = sql_db.Column(sql_db.Text, unique=True)
    password = sql_db.Column(sql_db.Text)
    user_role = sql_db.Column(sql_db.Text, default = "user")

    enabled = sql_db.Column(sql_db.Boolean, default = True)
    deleted = sql_db.Column(sql_db.Boolean, default = False)
    created_at = sql_db.Column(sql_db.DateTime, default=datetime.datetime.now)
    updated_at = sql_db.Column(sql_db.DateTime, default=datetime.datetime.now)

    def to_json(self):
        return_dict = {}
        return_dict['id'] = self.id
        return_dict['user_name'] = self.user_name
        return_dict['user_role'] = self.user_role

        return return_dict

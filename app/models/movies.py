from app.extensions import sql_db
import datetime

class MoviesData(sql_db.Model):
    #unique together on name + director
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    name = sql_db.Column(sql_db.Text, default = "")
    nn_popularity = sql_db.Column(sql_db.Float, default = 0.0)
    director = sql_db.Column(sql_db.Text, default = "")
    genre = sql_db.Column(sql_db.Text, default = "")
    imdb_score = sql_db.Column(sql_db.Float, default = 0.0)

    enabled = sql_db.Column(sql_db.Boolean, default = True)
    deleted = sql_db.Column(sql_db.Boolean, default = False)
    created_at = sql_db.Column(sql_db.DateTime, default=datetime.datetime.now)
    updated_at = sql_db.Column(sql_db.DateTime, default=datetime.datetime.now)

    def to_json(self):
        return_dict = {}
        return_dict['id'] = self.id
        return_dict['name'] = self.name
        return_dict['nn_popularity'] = self.nn_popularity
        return_dict['director'] = self.director
        return_dict['genre'] = self.genre
        return_dict['imdb_score'] = self.imdb_score

        return return_dict

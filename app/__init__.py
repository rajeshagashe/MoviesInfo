import os
import importlib

from flask import Flask
from flask_migrate import Migrate

from app.extensions import sql_db
from app.views import blueprints


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load global environments, when not testing
        print("|"* 100)
        print(os.environ)
        print("|"* 100)
        if os.path.exists("../.env"):
            app.config.from_pyfile("../.env")
        #connect db
        sql_db.init_app(app)
    else:
        app.config.from_pyfile("../.env")
        #connect db
        sql_db.init_app(app)
    
    for path, blueprint, url_prefix in blueprints:
        module = importlib.import_module(path)
        app.register_blueprint(getattr(module, blueprint), url_prefix=url_prefix)       
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

# migrations -->
# flask db init
# flask db migrate
# flask db upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate#, MigrateCommand
from app.models.movies import MoviesData 

app = create_app()
migrate = Migrate(app, sql_db)

from src import populate_movies_db

@app.cli.command('populate_db')
def populate_db():
    populate_movies_db.run()
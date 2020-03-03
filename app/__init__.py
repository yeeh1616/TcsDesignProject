from flask import Flask
from app import models
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

db = SQLAlchemy()


def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py',silent = True)
    else:
        app.config.from_pyfile('config_test.py',silent = True)

    #migrate = Migrate(app, db)
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import main_page
    app.register_blueprint(main_page.bp)

    return app





#from app import routes, model

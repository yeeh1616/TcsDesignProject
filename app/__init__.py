import app
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

print('Fuck 033')
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(test_config=None):
    print('Fuck 04')
    global db
    global login_manager

    app = Flask(__name__, instance_relative_config=True)
    login_manager.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile('config_test.py', silent=True)

    # migrate = Migrate(app, db)
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')
    from . import main_page
    app.register_blueprint(main_page.bp)

    print('Fuck 05')

    return app


print('Fuck 03')

if __name__ == '__main__':
    print('Fuck 01')
    app.run()

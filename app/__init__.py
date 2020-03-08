#import app
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

print('Fuck 033')
app = None
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
mail = Mail()


def create_app(test_config=None):
    print('Fuck 04')
    global db
    global login_manager
    global app

    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile('config_test.py', silent=True)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)



    # migrate = Migrate(app, db)


    from . import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')
    # from . import module
    # app.register_blueprint(module.bp)
    from . import homepage
    app.register_blueprint(homepage.bp)
    from . import module_info
    app.register_blueprint(module_info.bp, url_prefix='/module')
    print('Fuck 05')

    return app


print('Fuck 03')

if __name__ == '__main__':
    #print('Fuck 01')
    create_app()

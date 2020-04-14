import os
basedir = os.path.abspath(os.path.dirname(__file__))
#
#
# class Config(object):
#     # ...
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///../project_database'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SECRET_KEY = 'dev'
SECURITY_PASSWORD_SALT = 'should be safe'

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'testxiaxlc'
MAIL_PASSWORD = 'XiaLichen1998!'
MAIL_DEFAULT_SENDER = 'testxiaxlc@gmail.com'

from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/hello')
def hello():
    return "Hello, World!"


@bp.route('/')
@bp.route('/index')
def index():
    return "Homepage"
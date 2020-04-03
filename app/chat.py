from flask import Flask, Blueprint, render_template, request
from flask_login import login_required
from flask_socketio import SocketIO, send

from app import app
from app.decorators import check_confirmed
from app.models import Config

bp = Blueprint('chat', __name__, template_folder='templates/chat')
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@bp.route('/chat_page', methods=['GET', 'POST'])
@login_required
@check_confirmed
def chat_page():
    config = Config.get_config_by_key('server')
    config.ip = request.remote_addr
    return render_template('chat/chat.html', config=config)
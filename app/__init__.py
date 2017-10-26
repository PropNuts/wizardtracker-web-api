import eventlet
import threading
import time

from flask import Flask
from flask_socketio import SocketIO

from .data_streamer import DataStreamer


socketio = SocketIO()

data_streamer = DataStreamer(socketio)
data_streamer_thread = threading.Thread(target=data_streamer.start)


def init_rssi_streamer():
    if data_streamer_thread.is_alive():
        print('must stop')
        data_streamer.stop()
        data_streamer_thread.join()

    print('starting')
    data_streamer_thread.start()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a big secret'

    from .device_api import device_api
    app.register_blueprint(device_api, url_prefix='/device')

    socketio.init_app(app)
    return app

def run_app():
    eventlet.monkey_patch()

    app = create_app()
    init_rssi_streamer()

    socketio.run(app, debug=True)

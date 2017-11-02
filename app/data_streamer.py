import logging
import time
import socket
import socketio


LOGGER = logging.getLogger(__name__)


class DataStreamer:
    HOST = '127.0.0.1'
    PORT = 3092

    MESSAGES_PER_SECOND = 15

    def __init__(self, socketio):
        self._should_stop = False
        self._socketio = socketio

        self._sock = None
        self._sock_file = None

        self._last_message_time = time.clock()

    def start(self):
        self._sock = socket.create_connection(
            (DataStreamer.HOST, DataStreamer.PORT)
        )

        self._sock_file = self._sock.makefile()
        while not self._should_stop:
            self._loop()

    def stop(self):
        self._should_stop = True

    def _loop(self):
        data = self._sock_file.readline().strip()
        data_split = data.split(' ')

        timestamp = float(data_split[0]),
        rssi = [int(d) for d in data_split[1:]]

        if self._due_next_message():
            self._socketio.emit('rssi', {'rssi': rssi})
            self._last_message_time = time.clock()

    def _due_next_message(self):
        message_delay = 1 / DataStreamer.MESSAGES_PER_SECOND
        if time.clock() >= self._last_message_time + message_delay:
            return True
        else:
            return False

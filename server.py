import os, binascii
import json

import time

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import eventlet
eventlet.monkey_patch()

from quoter import Quoter

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*", engineio_logger=True)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('connect', 'Connected to Flask-SocketIO')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('parts')
def parts_quoter(parts):
    print(parts)
    parts_info = []
    total = len(parts)
    q = Quoter()
    for idx, part in enumerate(parts):
        progress = {
            'current': part['pn'],
            'total': total,
            'complete': idx
        }
        emit('progress', progress)
        info = q.part(part['pn'])
        if info: 
            info['qty'] = part['qty']
            info['vendor'] = 'Air Tractor'
        else:
            info = part
            info['desc'] = 'Not Found'
        parts_info.append(info)
        progress = {
            'current': part['pn'],
            'total': total,
            'complete': idx + 1
        }
    emit('partsInfo', parts_info)    


if __name__ == '__main__':
    socketio.run(app, debug=True)
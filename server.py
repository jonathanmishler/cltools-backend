import os, binascii
import json
import asyncio
import time

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import eventlet
eventlet.monkey_patch()

import rq_dashboard

from quoter import Quoter

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*", engineio_logger=True)

#setup rq dashboard
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")


@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('connect', 'Connected to Flask-SocketIO')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('get_quote')
def parts_quoter(parts):
    print(parts)
    q = Quoter()
    asyncio.run(quote_looper(q,parts))
    emit('received', f"Recieved {len(parts)} part numbers and sent to quoter process")    

async def quote_looper(q, parts_list):
    for part in parts_list:
        info = await q.part(part[1])
        data = {
            'index': part[0],
            'quote': info 
        }
        emit('partQuote', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
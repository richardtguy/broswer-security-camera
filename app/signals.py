"""
Signaling server

Simple signalling server using SocketIO to enable peers to find and establish a
connection.
"""

from flask import request
from flask_socketio import emit, send, join_room

from app import socketio

ROOM = 'room'

@socketio.on('connect')
def connect():
    print('Client connected')
    emit('ready', to=ROOM)
    join_room(ROOM)

@socketio.on('message')
def message(m):
    print(m)
    emit('message', m, to=ROOM)

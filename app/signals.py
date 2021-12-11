"""
Signaling server

Simple signalling server using SocketIO to enable peers to find and establish a
connection.
"""

from flask import request
from flask_socketio import emit, send, join_room

from app import socketio

broadcaster = None

@socketio.on('broadcaster')
def on_broadcaster():
    global broadcaster
    broadcaster = request.sid
    emit('broadcaster', broadcast=True)

@socketio.on('watcher')
def on_watcher():
    emit('watcher', request.sid, to=broadcaster)

@socketio.on('disconnect')
def on_disconnect():
    emit('disconnectPeer', request.sid, to=broadcaster)

@socketio.on('offer')
def on_offer(id, message):
    emit('offer', (request.sid, message), to=id)

@socketio.on('answer')
def on_offer(id, message):
    emit('answer', (request.sid, message), to=id)

@socketio.on('candidate')
def on_offer(id, message):
    emit('candidate', (request.sid, message), to=id)

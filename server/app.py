from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"
socket = SocketIO(app, cors_allowed_origins="*")

ACTIVE_USERS = 0

@app.route('/')
def hello():
    return render_template("index.html")

@socket.on("message")
def message(data):
    print(f"Received message: {data['message']}")
    now = datetime.today()
    fmt_time = now.strftime("%H:%M")
    msg = f"{fmt_time}: {data['message']}"

    emit("message", msg, room=data["gameId"])

@socket.on("connect")
def connect():
    print(f"[CLIENT CONNECTED]: {request.sid}")

@socket.on("disconnect")
def disconnect():
    print(f"[CLIENT DISCONNECTED]: {request.sid}")

@socket.on("send-clue")
def clue_sent(data):
    clue = data["clue"]
    print(clue)
    emit("send-clue", clue, room=data["gameId"])

@socket.on("join")
def join(data):
    game_id = data
    join_room(game_id)

if __name__ == "__main__":
    socket.run(app, debug=True)
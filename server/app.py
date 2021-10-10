from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime
import time
from game import Game

app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"
socket = SocketIO(app, cors_allowed_origins="*")

ACTIVE_USERS = 0
ROOMS = {}

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

@socket.on("make_move")
def make_move(data):
    print(f"got card {data['card']}")
    game = ROOMS[data["gameId"]]
    print("---")
    print(game.board)
    game.flip_card(data["card"]["name"])

    print("---")       
    print(game.board)
    emit("send-state", game.to_json(), room=data["gameId"])

@socket.on("create_game")
def create_game(gameId):
    game = Game()
    ROOMS[gameId] = game
    emit("create_game", game.to_json(), room=gameId)


if __name__ == "__main__":
    socket.run(app, debug=True)
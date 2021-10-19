from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime
import time
from game import Game
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"
socket = SocketIO(app, cors_allowed_origins="*")

ACTIVE_USERS = -1 # app counts as a connection???
ROOMS = {}

@app.route("/rand")
def rand():
    return str(random.randint(0, 100))

@app.route('/')
def hello():
    return str(random.randint(0, 100))
    # return render_template("index.html")

@socket.on("message")
def message(data):
    data["timestamp"] = datetime.today().strftime("%H:%M")
    emit("message", data, room=data["gameId"])

@socket.on("connect")
def connect():
    global ACTIVE_USERS
    ACTIVE_USERS += 1 
    print(f"\n\n[CLIENT CONNECTED]: {request.sid}")
    print(f"total connected users: {ACTIVE_USERS}\n\n")

@socket.on("disconnect")
def disconnect():
    global ACTIVE_USERS
    ACTIVE_USERS -= 1 
    print(f"\n\n[CLIENT DISCONNECTED]: {request.sid}")
    print(f"total connected users: {ACTIVE_USERS}\n\n")

@socket.on("send-clue")
def clue_sent(data):
    game = ROOMS[data["gameId"]] 
    clue = data["clue"]
    game.set_guesses(data["guesses"]) 
    game.current_clue = clue
    print("game:", game.board)
    emit("send-state", game.to_json(), room=data["gameId"])
    emit("send-clue", data, room=data["gameId"])

@socket.on("create_game")
def create_game(gameId):
    game = Game(gameId)
    ROOMS[gameId] = game
    print(f"create game with ID: {gameId}")
    # emit("create_game", game.to_json(), room=gameId)

@socket.on("join")
def join(data):
    game_id = data
    join_room(game_id)
    game = ROOMS[game_id]
    print(f"got game {game.board}")
    # get the game that is associated with the room here
    emit("before-join", game.to_json(), room=game_id)


@socket.on("make_move")
def make_move(data):
    game = ROOMS[data["gameId"]]
    print(data)
    if not data["correct"]:
        game.flip_card(data["card"]["name"])
        game.round += 1
        game.guesses = 0

        emit("send-state", game.to_json(), room=data["gameId"])
    else:
        game.flip_card(data["card"]["name"])
        game.decrement_guesses()

        emit("send-state", game.to_json(), room=data["gameId"])

if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=5000, debug=True)
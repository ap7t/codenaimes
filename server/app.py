from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime
import time
from game import Game

app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"
socket = SocketIO(app, cors_allowed_origins="*")

ACTIVE_USERS = -1 # app counts as a connection???
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
    print(">>>", game.guesses)
    game.current_clue = clue
    print(game.current_clue)
    print(game.to_json())
    emit("send-state", game.to_json(), room=data["gameId"])
    emit("send-clue", clue, room=data["gameId"])

@socket.on("join")
def join(data):
    print("--- Inside join func ---")
    game_id = data
    join_room(game_id)
    game = ROOMS[game_id]
    # get the game that is associated with the room here
    print(game)
    emit("send-state", game.to_json(), room=game_id)


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
        print(f"got card {data['card']}")
        print("+++ ", game.guesses)
        print("---")
        print(game.board)
        game.flip_card(data["card"]["name"])
        game.decrement_guesses()

        print("---")       
        print(game.board)
        emit("send-state", game.to_json(), room=data["gameId"])

@socket.on("create_game")
def create_game(gameId):
    game = Game(gameId)
    ROOMS[gameId] = game
    print(game)
    # emit("create_game", game.to_json(), room=gameId)

if __name__ == "__main__":
    socket.run(app, debug=True)
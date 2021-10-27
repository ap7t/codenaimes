from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime, timedelta
from game import Game
from user import User
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
    # netsoc cloud time in utc, maybe use some js lib for showing time on frontend
    data["timestamp"] = (datetime.today() + timedelta(hours=1)).strftime("%H:%M") 
    emit("message", data, room=data["gameId"])

@socket.on("connect")
def connect():
    global ACTIVE_USERS
    ACTIVE_USERS += 1 
    print(f"\n\n[CLIENT CONNECTED]: {request.sid}")
    print(f"total connected users: {ACTIVE_USERS}\n\n")

@socket.on("disconnect")
def disconnect():
    for game in ROOMS.values():
        print(game)
        if game.has_user(request.sid):
            user = game.delete_user(request.sid)
            emit("user_leave", user.__dict__, room=game.id)
            emit("send-state", game.to_json(), room=game.id)
            

@socket.on("send-clue")
def clue_sent(data):
    game = ROOMS[data["gameId"]] 
    clue = data["clue"]
    game.set_guesses(data["guesses"] + 1)
    game.current_clue = clue
    print("game:", game.board)
    emit("send-state", game.to_json(), room=data["gameId"])
    emit("send-clue", data, room=data["gameId"])

@socket.on("create_game")
def create_game(gameId):
    # check game doesn't exist:
    print(request.sid)
    if gameId in ROOMS.keys():
        emit("cant_create", roonm=request.sid)
    else:
        game = Game(gameId)
        ROOMS[gameId] = game
        emit("create_game", room=request.sid)

@socket.on("join")
def join(data):
    gameId = data
    join_room(gameId)
    game = ROOMS[gameId]
    # get the game that is associated with the room here
    emit("before-join", game.to_json(), room=gameId)


@socket.on("make_move")
def make_move(data):
    game = ROOMS[data["gameId"]]
    if not data["correct"]:
        game.flip_card(data["card"]["name"])
        game.end_round() 
        emit("send-state", game.to_json(), room=data["gameId"])
    else:
        game.flip_card(data["card"]["name"])
        game.decrement_guesses()

        emit("send-state", game.to_json(), room=data["gameId"])

@socket.on("end_round")
def end_round(gameId):
    game = ROOMS[gameId]
    game.end_round()
    emit("send-state", game.to_json(), room=gameId)


@socket.on("game_over")
def game_over(gameId):
    game = ROOMS[gameId]
    game.over = True

@socket.on("user_join") 
def user_join(data):
    game = ROOMS[data["gameId"]]
    user = User(request.sid, data["name"], data["team"], data["role"])
    game.add_user(user)
    emit("user_join", user.__dict__, room=data["gameId"])
    emit("send-state", game.to_json(), room=data["gameId"])

@socket.on("user_leave") 
def user_leave(data):
    game = ROOMS[data["gameId"]]
    user = game.delete_user(request.sid)
    emit("user_leave", user.__dict__, room=data["gameId"])
    emit("send-state", game.to_json(), room=data["gameId"])
    
if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=5000, debug=True)
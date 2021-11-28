from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime, timedelta
from game import Game
from user import User
import random
import pickle
from ai.word2vec import Word2Vec
from ai.spymaster import Spymaster
import time

# Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"

# Web sockets
socket = SocketIO(app, cors_allowed_origins="*")

# word2vec
word2vec = Word2Vec()
# with open("./ai/word2vec.obj", "rb") as f:
    # word2vec = pickle.load(f)



ACTIVE_USERS = -1 # app counts as a connection???
ROOMS = {}
AI_ROOMS = {}

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
    if gameId in ROOMS.keys() or gameId in AI_ROOMS.keys():
        emit("cant_create", roonm=request.sid)
    else:
        game = Game(gameId)
        ROOMS[gameId] = game
        emit("create_game", room=request.sid)

@socket.on("ai_create_game")
def ai_create_game(gameId):
    # check game doesn't exist:
    print(request.sid)
    if gameId in AI_ROOMS.keys() or gameId in ROOMS.keys():
        print("already exists")
        emit("ai_cant_create", room=request.sid)
    else:
        print("making ai spymaster")
        t = time.time()
        game = Game(gameId)
        red_clues = word2vec.generate_clues(game, "red")
        blue_clues = word2vec.generate_clues(game, "blue")
        spymaster = Spymaster(gameId, red_clues, blue_clues)
        AI_ROOMS[gameId] = {"game": game, "spymaster": spymaster}
        print("done making ai spymaster: ", (time.time() - t) / 60)
        emit("ai_create_game", room=request.sid)

@socket.on("join")
def join(data):
    gameId = data
    join_room(gameId)
    game = ROOMS[gameId]
    # get the game that is associated with the room here
    emit("before-join", game.to_json(), room=gameId)

@socket.on("ai_join")
def join(data):
    gameId = data
    join_room(gameId)
    game = AI_ROOMS[gameId]["game"]
    # get the game that is associated with the room here
    emit("before-join", game.to_json(), room=gameId)

@socket.on("request-clue")
def request_clue(data):
    print("requesting clue")
    gameId = data["gameId"]
    game = AI_ROOMS[gameId]["game"]
    print(AI_ROOMS)
    print(game.board)
    spymaster = AI_ROOMS[gameId]["spymaster"]
    team = data["team"]
    if team == "Red":
        clue = spymaster.generate_red_clue(game.remaining_agents("red"))
    else:
        clue = spymaster.generate_blue_clue(game.remaining_agents("blue"))
    data["clue"] = clue[0]
    game.set_guesses(len(clue[1]) + 1)
    game.current_clue = clue[0]
    print(game.current_clue)
    emit("send-state", game.to_json(), room=data["gameId"])
    emit("send-clue", data, room=data["gameId"])

@socket.on("make_move")
def make_move(data):
    if data["ai"]:
        game = AI_ROOMS[data["gameId"]]["game"]
    else:
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
def end_round(data):
    if data["ai"]:
        game = AI_ROOMS[data["gameId"]]["game"]
    else:
        game = ROOMS[data["gameId"]]
    game.end_round()
    emit("send-state", game.to_json(), room=data["gameId"])


@socket.on("game_over")
def game_over(gameId):
    game = ROOMS[gameId]
    game.over = True

@socket.on("user_join") 
def user_join(data):
    game = ROOMS[data["gameId"]]
    print(game.id)
    user = User(request.sid, data["name"], data["team"], data["role"])
    game.add_user(user)
    emit("user_join", user.__dict__, room=data["gameId"])
    emit("send-state", game.to_json(), room=data["gameId"])

@socket.on("ai_user_join") 
def ai_user_join(data):
    game = AI_ROOMS[data["gameId"]]["game"]
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

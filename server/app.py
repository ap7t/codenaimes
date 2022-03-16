from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room
from datetime import datetime, timedelta
from game import Game
from user import User
import random
import pickle
from ai.word2vec import Word2Vec
from ai.glove import Glove
from ai.spymaster import Spymaster
import time
from experiment import Experiment
import pickle


# Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "changeme"
print("hello from flask")

# Web sockets
socket = SocketIO(app, cors_allowed_origins="*")

# word2vec
word2vec = Word2Vec()
print("made word2vec")
# with open("./ai/word2vec.obj", "rb") as f:
    # word2vec = pickle.load(f)

#GloVe
glove = Glove()
print("made glove")
# with open("./ai/word2vec.obj", "rb") as f:



ACTIVE_USERS = -1 # app counts as a connection???
ROOMS = {}
AI_ROOMS = {}
EXPERIMENTS = {}

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
        spymaster = Spymaster(gameId, game.red_agents, game.blue_agents, word2vec)
        AI_ROOMS[gameId] = {"game": game, "spymaster": spymaster}
        print("done making ai spymaster: ", (time.time() - t) / 60)
        emit("ai_create_game", room=request.sid)

@socket.on("join")
def join(data):
    gameId = data
    join_room(gameId)
    game = ROOMS[gameId]
    print(game.solution)
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
    # print(game.board)
    spymaster = AI_ROOMS[gameId]["spymaster"]
    team = data["team"]
    print(team)
    if team == "red":
        clue = spymaster.generate_red_clue(2, 1, game.remaining_agents("red"))
    else:
        clue = spymaster.generate_blue_clue(2,1, game.remaining_agents("blue"))
    data["clue"] = clue[0]
    print(f"Generated: {clue}")
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

@socket.on("refresh")
def refresh(gameId):
    print("refreshing")
    game = ROOMS[gameId]
    game.over = False
    game.create_game()
    emit("send-state", game.to_json(), room=gameId)

@socket.on("user_leave") 
def user_leave(data):
    game = ROOMS[data["gameId"]]
    user = game.delete_user(request.sid)
    emit("user_leave", user.__dict__, room=data["gameId"])
    emit("send-state", game.to_json(), room=data["gameId"])

# ##########
# Experiment
# ##########
@socket.on("experiment-create")
def experiment_create(expId):
    print("##### making experiment #####")
    print("expId: ", expId)
    e = Experiment(expId, word2vec)
    EXPERIMENTS[expId] = e
    # e.generate_clue()
    # emit("send-experiment", data, room=request.sid)
    print("sending exp")
    emit("before-experiment-join", e.game.to_json(), room=request.sid)

@socket.on("experiment")
def experiment(expId):
    e = EXPERIMENTS[expId]
    clue = e.generate_clue()
    print("clue: ", clue)
    print("sending-clue")
    emit("send-experiment", clue, room=request.sid)

@socket.on("send-answer")
def send_experiment(data):
    print(data)
    e = EXPERIMENTS[data["expId"]]
    e.make_guess(data["word1"], data["word2"], data["word3"], data["word4"])
    clue = e.generate_clue()
    print(e.game.board)
    print(zip(e.clues, e.guesses))
    emit("send-experiment", clue, room=request.sid)
    

@socket.on("experiment-create-spymaster")
def experiment_create_spymaster(expId):
    e = EXPERIMENTS[expId]
    print(">>> yes")
    emit("before-experiment-join-spymaster", e.game2.to_json(), room=request.sid)

@socket.on("experiment-spymaster")
def experiment(expId):
    e = EXPERIMENTS[expId]
    words = e.generate_spymaster_words()
    print("words: ", words)
    print("sending-clue")
    data = {"word1": words[0], "word2": words[1]}
    print(f"data: {data}")
    emit("send-experiment-spymaster", data, room=request.sid)


@socket.on("send-answer-spymaster")
def send_experiment(data):
    print(data)
    e = EXPERIMENTS[data["expId"]]
    e.take_spymaster_clue(data["clue"])
    words = e.generate_spymaster_words()
    print("clue: ", words)
    data = {"word1": words[0], "word2": words[1]}
    print(f"data: {data}")
    emit("send-experiment-spymaster", data, room=request.sid)

@socket.on("save-experiment")
def save_experiment(expId):
    e = EXPERIMENTS[expId]
    with open(f"results/{e.id}.pkl", "wb") as f:
        pickle.dump(e, f)
    
if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=5000, debug=True)

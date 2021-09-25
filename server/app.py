from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
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
def message(msg):
    print(f"Received message: {msg}")
    now = datetime.today()
    fmt_time = now.strftime("%H:%M")
    msg = f"{fmt_time}: {msg}"

    send(msg, broadcast=True)

@socket.on("connect")
def connect():
    print(f"[CLIENT CONNECTED]: {request.sid}")

@socket.on("disconnect")
def disconnect():
    print(f"[CLIENT DISCONNECTED]: {request.sid}")

@socket.on("notify")
def notify(user):
   emit("notify", user, broadcast=True, skip_sid=request.sid) 


if __name__ == "__main__":
    socket.run(app, debug=True)
from player import Player

RED_TEAM = "red"
BLUE_TEAM = "blue"

class Teams:
    def __init__(self, team):
        self.red = {"spymasters": [], "operatives": []}
        self.blue = {"spymasters": [], "operatives": []}

    def add_spymaster(self, sid, name, team):
        p = Player(sid, name)
        if team == RED_TEAM:
            self.red["spymaster"].append(p)
        elif team == BLUE_TEAM:
            self.blue["spymaster"].append(p)

    def add_operative(self, sid, name, team):
        p = Player(sid, name)
        if team == RED_TEAM:
            self.red["operative"].append(p)
        elif team == BLUE_TEAM:
            self.blue["operative"].append(p)

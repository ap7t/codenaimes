from datetime import datetime
from random import shuffle

RED = "R"
BLUE = "B"
CIVILIAN = "O"
ASSASSIN = "X"

TOTAL_PLAYERS = 25
AGENTS_PER_TEAM = 8
TOTAL_ASSASSINS = 1
TOTAL_CIVLIANS = TOTAL_PLAYERS - (AGENTS_PER_TEAM * 2 + 1 + TOTAL_ASSASSINS)

with open("agents.txt", "r") as f:
    agents = f.read().split("\n")

agents.pop()


class Game:
    def __init__(self, id="dev"):
        self.id = id
        self.start_colour = RED
        self.date_created = datetime.now()
        # TODO: self.players = players
        self.round = 0
        self.total_guesses = 0
        self.guesses = 0
        self.num_red_agents = AGENTS_PER_TEAM + 1
        self.num_blue_agents = AGENTS_PER_TEAM
        self.assassinated = False
        self.board = None
        self.solution = None
        self.over = False
        self.current_clue = None
        self.users = {}
        self.create_board()
        self.red_agents = self.get_agents("R")
        self.blue_agents = self.get_agents("B")
        self.civilians = self.get_agents("O")
        self.assassin = self.get_agents("X")
        self.history = ""

    def to_json(self):
        return {
            "gameId": self.id,
            "start_colour": self.start_colour,
            "board": self.board,
            "solution": self.solution,
            "date_created": str(self.date_created),
            "red_agents": self.num_red_agents,
            "blue_agents": self.num_blue_agents,
            "assassinated": self.assassinated,
            "round": self.round,
            "guesses": self.guesses,
            "current_clue": self.current_clue,
            "users": len(self.users),
            "history": self.history
        }

    def create_board(self):
        """
            Creates the game board
        """
        words = self.generate_words()
        positions = self.generate_positions()
        solution = zip(words, positions)
        self.board = dict.fromkeys(words, False)
        self.solution = dict(solution)

    def generate_words(self):
        shuffle(agents)  # newline in file is empty string
        return agents[:TOTAL_PLAYERS]

    def generate_positions(self):
        # TODO: not always red starting
        positions = [RED] * (AGENTS_PER_TEAM + 1)
        positions.extend([BLUE] * AGENTS_PER_TEAM)
        positions.extend([ASSASSIN] * TOTAL_ASSASSINS)
        positions.extend([CIVILIAN] * TOTAL_CIVLIANS)
        shuffle(positions)
        return positions

    def duration(self):
        start = self.date_created
        now = self.date_last_updated
        time_delta = now - start
        print(time_delta.seconds)

    def flip_card(self, word):
        self.date_last_updated = datetime.now()
        if self.solution[word] == RED and not self.board[word]:
            self.num_red_agents -= 1
        elif self.solution[word] == BLUE and not self.board[word]:
            self.num_blue_agents -= 1
        elif self.solution[word] == ASSASSIN and not self.board[word]:
            self.assassinated = True
        self.board[word] = self.solution[word]
        print(self.board[word])
        # TODO: make rounds more than just one guess

    def decrement_guesses(self):
        self.guesses -= 1
        if self.guesses == 0:
            self.round += 1

    def set_guesses(self, guesses):
        self.guesses = guesses

    def end_round(self):
        self.round += 1
        self.guesses = 0

    def add_user(self, user):
        self.users[user.sid] = user

    def delete_user(self, sid):
        return self.users.pop(sid)

    def has_user(self, sid):
        return True if sid in self.users.keys() else False

    def get_agents(self, colour):
        return [agent.lower() for agent, col in self.solution.items() if col == colour]

    def remaining_agents(self, team):
        agents = self.red_agents if team == "red" else self.blue_agents
        return [a for a in agents if not self.board[a.upper()]]

    def __str__(self):
        return str(self.solution)


if __name__ == "__main__":
    g = Game()
    g.create_board()

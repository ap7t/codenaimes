from mimetypes import init

from game import Game
from ai.spymaster import Spymaster
from ai.word2vec import Word2Vec

class Experiment:
    def __init__(self, id, embedding):
        self.id = id
        self.game = Game(id)
        self.spymaster = Spymaster(id, self.game.red_agents, self.game.blue_agents, embedding)
       
        self.game2 = Game(id)
        self.spymaster2 = Spymaster(id, self.game2.red_agents, self.game2.blue_agents, embedding)

        self.clues = [] # list of tuples from spymaster
        self.guesses = [] # list of tuples from top 4 guesses

        self.spymaster_clues = []
        self.given_spymaster_clues = []


    def generate_clue(self):
        clue = self.spymaster.generate_blue_clue(2, 1, self.game.remaining_agents("blue"))
        self.clues.append(clue)
        print(f"\n\clue for operative: {clue}\n")
        return clue[0]

    def make_guess(self, word1, word2, word3=None, word4=None):
        guesses = [word1, word2, word3, word4]
        self.guesses.append(guesses)
        self.update_board()

    def get_percision(self):
        # TODO: check lower case from sent words 
        total = 0
        correct = 0
        for i in range(len(self.guesses)):
            total += 2
            if self.guesses[i][0] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][1] in self.clues[i][1]:
                correct += 1
            
        return correct


    def get_precision(self):
        total = 0
        correct = 0
        for i in range(len(self.guesses)):
            total += 4
            if self.guesses[i][0] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][1] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][2] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][3] in self.clues[i][1]:
                correct += 1
            
            
        return correct

    def update_board(self):
        for clue in self.clues:
            first = clue[1][0].upper()
            second = clue[1][0].upper()
            if not self.game.board[first]:
                self.game.flip_card(first)
            if not self.game.board[second]:
                self.game.flip_card(second)


    def generate_spymaster_words(self):
        clue = self.spymaster2.generate_red_clue(2, 1, self.game2.remaining_agents("blue"))
        self.spymaster_clues.append(clue)
        print(f"\n\nspymaster clues: {self.spymaster_clues}\n\n")
        return clue[1]
    
    def take_spymaster_clue(self, clue):
        self.given_spymaster_clues.append(clue)
        self.update_board_spymaster()

    def update_board_spymaster(self):
        for clue in self.spymaster_clues:
            first = clue[1][0].upper()
            second = clue[1][1].upper()
            print(f"first: {first}, second: {second}")
            if not self.game2.board[first]:
                self.game2.flip_card(first)
            if not self.game2.board[second]:
                self.game2.flip_card(second)
 



    


if __name__ == "__main__":
    e = Experiment(1)

from distutils.command.clean import clean
from mimetypes import init

from game import Game
from ai.spymaster import Spymaster
from ai.word2vec import Word2Vec


class Experiment:
    def __init__(self, id, embedding):
        self.embdedding = embedding
        self.id = id
        self.game = Game(id)
        self.spymaster = Spymaster(
            id, self.game.red_agents, self.game.blue_agents, embedding)

        self.game2 = Game(id)
        self.spymaster2 = Spymaster(
            id, self.game2.red_agents, self.game2.blue_agents, embedding)

        self.clues = []  # list of tuples from spymaster
        self.guesses = []  # list of tuples from top 4 guesses

        self.spymaster_clues = []
        self.given_spymaster_clues = []

    def generate_clue(self):
        clue = self.spymaster.generate_blue_clue(
            2, 1, self.game.remaining_agents("blue"))
        self.clues.append(clue)
        print(f"\n\clue for operative: {clue}\n")
        return clue[0]

    def make_guess(self, word1, word2, word3=None, word4=None):
        guesses = [word1, word2, word3, word4]
        self.guesses.append(list(map(lambda x: x.lower(), guesses)))
        self.update_board()

    def get_percision(self):
        total = 0
        correct = 0
        for i in range(len(self.guesses)):
            total += 2
            if self.guesses[i][0] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][1] in self.clues[i][1]:
                correct += 1

        return correct/total

    def get_precision_per_round(self):
        ps = []
        for i in range(len(self.guesses)):
            correct = 0
            if self.guesses[i][0] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][1] in self.clues[i][1]:
                correct += 1
            ps.append(correct/2)

        return ps

    def get_recall(self):
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

        return correct/total

    def get_recall_per_round(self):
        rs = []
        for i in range(len(self.guesses)):
            correct = 0
            if self.guesses[i][0] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][1] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][2] in self.clues[i][1]:
                correct += 1
            if self.guesses[i][3] in self.clues[i][1]:
                correct += 1

            rs.append(correct/4)
        return rs

    def update_board(self):
        for clue in self.clues:
            first = clue[1][0].upper()
            second = clue[1][0].upper()
            if not self.game.board[first]:
                self.game.flip_card(first)
            if not self.game.board[second]:
                self.game.flip_card(second)

    def generate_spymaster_words(self):
        clue = self.spymaster2.generate_blue_clue(
            2, 1, self.game2.remaining_agents("blue"))
        self.spymaster_clues.append(clue)
        print(f"\n\nspymaster clues: {self.spymaster_clues}\n\n")
        return clue[1]

    def take_spymaster_clue(self, clue):
        self.given_spymaster_clues.append(clue.lower())
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

    def results(self):
        tmp_str = "+--- Phase 1 ---+\n"
        cs = []
        for clue in self.clues[:-1]:
            c = f"{clue[0][0]:20}"
            cs.append(c)
        tmp_str += f"+ {'Clue:':13} + " + " + ".join(cs) + "+\n"
        exp = []
        for clue in self.clues[:-1]:
            ws = f"{clue[1][0]} | {clue[1][1]}"
            w = f"{ws:20}"
            exp.append(w)
        tmp_str += f"+ {'Expected:':13} + " + " + ".join(exp) + "+\n"
        top_two = []
        for guess in self.guesses:
            gs = f"{guess[0]} | {guess[1]}"
            g = f"{gs:20}"
            top_two.append(g)
        tmp_str += f"+ {'Top 2:':13} + " + " + ".join(top_two) + "+\n"
        other_two = []
        for guess in self.guesses:
            gs = f"{guess[2] if guess[2] else '__'} | {guess[3] if guess[3] else '__'}"
            g = f"{gs:20}"
            other_two.append(g)
        tmp_str += f"+ {'Bottom 2:':13} + " + " + ".join(other_two) + "+\n"
        precision_per_round = self.get_precision_per_round()
        ps = []
        for p in precision_per_round:
            s = f"{p:20}"
            ps.append(s)
        tmp_str += f"+ {'precision@2:':13} + " + " + ".join(ps) + "+\n"
        recall_per_round = self.get_recall_per_round()
        ps = []
        for p in recall_per_round:
            s = f"{p:20}"
            ps.append(s)
        tmp_str += f"+ {'recall@4:':13} + " + " + ".join(ps) + "+\n"
        tmp_str += "+--- Phase 2 ---+\n"
        words = []
        for clue in self.spymaster_clues:
            if clue:
                cs = f"{clue[1][0]} | {clue[1][1]}"
                c = f"{cs:20}"
                words.append(c)
        tmp_str += f"+ {'Words: ':13} + " + " + ".join(words) + " +\n"
        ais = []
        for clue in self.spymaster_clues:
            if clue:
                ai = f"{clue[0][0]:20}"
                ais.append(ai)
        tmp_str += f"+ {'AI clue:':13} + " + " + ".join(ais) + "+\n"

        cs = []
        for clue in self.given_spymaster_clues:
            c = f"{clue:20}"
            cs.append(c)

        tmp_str += f"+ {'Human clue:':13} + " + \
            " + ".join(cs) + " +\n"
        sims = []
        for i in range(len(self.given_spymaster_clues)):
            ai = self.spymaster_clues[i][0][0]  # comes back as list
            human = self.given_spymaster_clues[i]
            sim = self.embdedding.get_word_similarity(human, ai)
            sims.append(f'{sim:20}')
        tmp_str += f"+ {'Similarity:':13} + " + " + ".join(sims) + " +\n"
        print(tmp_str)


"""
+---++---+
+--- Phase 1 ---+
+ Round 1 + Round 2 + ... + Round 5 +
+ Clue: clue + ...
+ Expected words: w1 w2
+ Given w1, w2,
+ Optional w2, w2
+---+
+ Phase 2 +
+ Round 1 ...
+ AI clue: w1
+ Human clue: w2
+ Similarity: s1


"""


if __name__ == "__main__":
    e = Experiment(1)

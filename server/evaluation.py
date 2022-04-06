import pickle
import os


class Evaluation:
    def __init__(self, exp):
        self.e = exp
        self.votes = []

    def get_game_words(self):
        return [t[1] for t in self.e.spymaster_clues if t]

    def get_ai_clues(self):
        return [t[0][0] for t in self.e.spymaster_clues if t]

    def get_human_clues(self):
        return self.e.given_spymaster_clues

    def make_vote(self, vote):
        self.votes.append(vote)

    # def get_words_and_clues(self):
    #     a = e.get_game_words()
    #     b = e.get_ai_clues()
    #     c = e.get_human_clues()
    #     return zip(a,b,c)


if __name__ == "__main__":
    files = [
        f"results/{f}" for f in os.listdir("./results/") if os.path.isfile(f"results/{f}")]
    file = files[0]
    with open(file, "rb") as f:
        exp = pickle.load(f)
        print(f"--- File: {file} ---")
        e = Evaluation(exp)

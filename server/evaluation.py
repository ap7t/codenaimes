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

    def calc_human_percent(self):
        total = 0
        human = 0
        for i in range(len(self.e.given_spymaster_clues)):
            total += 1
            if self.e.given_spymaster_clues[i].lower() == self.votes[i].lower():
                human += 1

        return human/total * 100

    def calc_ai_percent(self):
        return 100 - self.calc_human_percent()

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


class GroupEvaluation:
    def __init__(self, evals):
        self.evals = evals

    def calc_total_ai_percent(self):
        return 100 - self.calc_total_human_percent()

    def calc_total_human_percent(self):
        total = 0
        human = 0
        for eval in self.evals:
            for i in range(len(eval.e.given_spymaster_clues)):
                total += 1
                if eval.e.given_spymaster_clues[i].lower() == eval.votes[i].lower():
                    human += 1

        return round(human/total * 100)

    def results(self):
        for i, eval in enumerate(self.evals):
            tmp_str = f"+--- Board {i} ---+\n"
            exp = []
            for word in eval.e.spymaster_clues[:-1]:
                ws = f"{word[1][0]} | {word[1][1]}"
                w = f"{ws:20}"
                exp.append(w)
            tmp_str += f"+ {'Words:':13} + " + " + ".join(exp) + "+\n"

            cs = []
            for clue in eval.e.spymaster_clues[:-1]:
                c = f"{clue[0][0]:20}"
                cs.append(c)
            tmp_str += f"+ {'AI:':13} + " + " + ".join(cs) + "+\n"

            hs = []
            for clue in eval.e.given_spymaster_clues:
                h = f"{clue:20}"
                hs.append(h)
            tmp_str += f"+ {'Human:':13} + " + " + ".join(hs) + "+\n"

            vs = []
            for vote in eval.votes:
                v = f"{vote:20}"
                vs.append(v)
            tmp_str += f"+ {'Voted:':13} + " + " + ".join(vs) + "+\n"

            tmp_str += f"+ {'AI chosen':13} + {eval.calc_ai_percent()}%\n"
            tmp_str += f"+ {'Human chosen':13} + {eval.calc_human_percent()}%\n"
            print(tmp_str)

     

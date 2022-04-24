from game import Game
from ai.spymaster import Spymaster
from ai.word2vec import Word2Vec
from experiment import Experiment

import pickle
import os

files = [
    f"evaluations/{f}" for f in os.listdir("./evaluations/") if os.path.isfile(f"evaluations/{f}")]

total = 0
human = 0

for file in files:
    with open(file, "rb") as f:
        g = pickle.load(f)
        for eval in g.evals:
            for i in range(len(eval.e.given_spymaster_clues)):
                total += 1
                if eval.e.given_spymaster_clues[i].lower() == eval.votes[i].lower():
                    human += 1

print("Human", round(human/total * 100))
print("AI", 100-round(human/total * 100))

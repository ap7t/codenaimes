from game import Game
from ai.spymaster import Spymaster
from ai.word2vec import Word2Vec
from evaluation import GroupEvaluation

import pickle
import os

files = [
    f"evaluations/{f}" for f in os.listdir("./evaluations/") if os.path.isfile(f"evaluations/{f}")]

for file in files:
    with open(file, "rb") as f:
        g = pickle.load(f)
        print(f"--- File: {file} ---")
        g.results()
        tmp_str = "+--- Total ---+\n"
        tmp_str += f"+ {'AI chosen':13} + {g.calc_total_ai_percent()}%\n"
        tmp_str += f"+ {'Human chosen':13} + {g.calc_total_human_percent()}%\n"
        print(tmp_str)

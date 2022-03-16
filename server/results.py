from game import Game
from ai.spymaster import Spymaster
from ai.word2vec import Word2Vec
from experiment import Experiment

import pickle
import os

files = [ f"results/{f}" for f in os.listdir("./results/") if os.path.isfile(f"results/{f}")]

for file in files:
    with open(file, "rb") as f:
        e = pickle.load(f)
        print(f"--- File: {file} ---")
        print(f"Guesses: {e.guesses}")
        print(f"Given clues: {e.given_spymaster_clues}")
        print(f"Precision@2: {e.get_precision()}")



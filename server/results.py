from game import Game
from ai.spymaster import Spymaster
from ai.word2vec import Word2Vec
from experiment import Experiment

import pickle
import os

files = [
    f"results/{f}" for f in os.listdir("./results/") if os.path.isfile(f"results/{f}")]

for file in files:
    with open(file, "rb") as f:
        e = pickle.load(f)
        print(f"--- File: {file} ---")
        e.results()

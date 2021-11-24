from gensim.models import KeyedVectors
import itertools
import operator

class Word2Vec:
    # save to file to speed up things
    def __init__(self):
        # filename = "GoogleNews-vectors-negative300.bin"
        filename = "data/GoogleNews-vectors-negative300.bin"
        self.model = KeyedVectors.load_word2vec_format(filename, binary=True)
        
    def generate_clues(self, game, team="red"):
        ours = game.red_agents if team == "red" else game.blue_agents
        theirs = game.blue_agents if team == "red" else game.red_agents

        clues = {}
        for our1, our2 in itertools.combinations(ours, r=2):
            our_list = [our1, our2]
            # TODO: doesnt avoid similar to enemy as was giving strange results
            candidates = [(c.lower(), s) for c,s in self.model.most_similar(positive=our_list, topn=50)]
            clues[(our1, our2)] = [c for c,_ in candidates if self.is_valid(c, our_list)][:10]
        return clues
    
    def is_valid(self, clue, possible_clues):
        if "_" in clue:
            return False
        for poss in possible_clues:
            if poss in clue or clue in poss:
                return False
        return True

if __name__ == "__main__":
    import pickle

    w = Word2Vec()
    with open("word2vec.obj", "wb") as f:
        pickle.dump(w, f)

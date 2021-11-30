from gensim.models import KeyedVectors
import itertools
import operator

class Word2Vec:
    # save to file to speed up things
    def __init__(self):
        # filename = "GoogleNews-vectors-negative300.bin"
        filename = "data/GoogleNews-vectors-negative300.bin"
        self.model = KeyedVectors.load_word2vec_format(filename, binary=True, limit = 500000)
        
    def get_weighted_nn(self, word, n=500):
        nn_w_similarities = {}

        # if word not in self.model.vocab:
        #     return nn_w_similarities
        neighbours_and_similarities = self.model.most_similar(word, topn=n)
        for neighbour, similarity in neighbours_and_similarities:
            if len(neighbour.split("-")) > 1 or len(neighbour.split("-")) > 1:
                continue
            neighbour  = neighbour.lower()
            if neighbour not in nn_w_similarities:
                nn_w_similarities[neighbour] = similarity
            nn_w_similarities[neighbour] = max(similarity, nn_w_similarities[neighbour])
            
        return {k:v for k,v in nn_w_similarities.items() if k != word}

    def penalise(self, chosen_words, potential_clue, agents):
        max_similarity = float("-inf")
        if potential_clue not in self.model:
            return 0.0
        
        for agent in agents:
            if agent in self.model:
                similarity = self.model.similarity(agent, potential_clue)
                if similarity > max_similarity:
                    max_similarity = similarity
    
        return -0.5*max_similarity

    def dict2vec_embedding_weight(self):
        return 2.0

    def get_word_similarity(self, word1, word2):
        try:
            return 2.0
        except KeyError:
            return -1.0



if __name__ == "__main__":
    import pickle

    w = Word2Vec()
    with open("word2vec.obj", "wb") as f:
        pickle.dump(w, f)

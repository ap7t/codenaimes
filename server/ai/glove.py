from gensim.models import KeyedVectors


class Glove():

    def __init__(self, configuration=None):
        filename = "data/glove.6B.300d.txt"
        self.model = KeyedVectors.load_word2vec_format(filename, limit=500000)

    def get_weighted_nn(self, word, n=500):
        nn_w_similarities = {}

        # if word not in self.model.vocab:
        #     return nn_w_similarities
        neighbors_and_similarities = self.model.most_similar(
            word, topn=n)
        for neighbor, similarity in neighbors_and_similarities:
            if len(neighbor.split("_")) > 1 or len(neighbor.split("-")) > 1:
                continue
            neighbor = neighbor.lower()
            if neighbor not in nn_w_similarities:
                nn_w_similarities[neighbor] = similarity
            nn_w_similarities[neighbor] = max(
                similarity, nn_w_similarities[neighbor])

        return {k: v for k, v in nn_w_similarities.items() if k != word}

    def penalise(self, chosen_words, potential_clue, agents):
        similarity = float("-inf")
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
            return self.model.similarity(word1, word2)
        except KeyError:
            return -1.0

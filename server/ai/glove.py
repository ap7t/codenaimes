from gensim.models import KeyedVectors


class Glove():

    def __init__(self, configuration=None):
        filename = "data/glove.840B.300d.txt"
        self.model = KeyedVectors.load_word2vec_format(filename, limit=700000)

    def get_weighted_nn(self, word, n=500):
        nn_w_similarities = {}

        if word not in self.glove_model.vocab:
            return nn_w_similarities
        neighbors_and_similarities = self.glove_model.most_similar(
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

    def penalise(self, chosen_words, potential_clue, red_words):
        similarity = float("-inf")
        if potential_clue not in self.glove_model:
            if self.configuration.verbose:
                print("Potential clue word ",
                      potential_clue, "not in glove model")
            return 0.0

        for red_word in red_words:
            if red_word in self.glove_model:
                similarity = self.glove_model.similarity(
                    red_word, potential_clue)
                if similarity > similarity:
                    similarity = similarity

        if self.configuration.debug_file:
            with open(self.configuration.debug_file, 'a') as f:
                f.write(" ".join([str(x) for x in [
                        " glove penalty for red words:", similarity, "\n"
                        ]]))
        return -0.5*similarity

    def dict2vec_embedding_weight(self):
        return 2.0

    def get_word_similarity(self, word1, word2):
        try:
            return self.glove_model.similarity(word1, word2)
        except KeyError:
            return -1.0

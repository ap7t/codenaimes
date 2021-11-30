import itertools
import heapq
from nltk.stem import PorterStemmer

class Spymaster:
    def __init__(self, id, red_words, blue_words, word2vec):
        self.id = id
        self.red_words = red_words
        self.blue_words = blue_words
        self.words = self.red_words + self.blue_words
        self.embedding = word2vec
        self.weighted_nn = dict()
        self.stemmer = PorterStemmer()
        self.used_clues = []
        for word in self.words:
            self.weighted_nn[word] = self.embedding.get_weighted_nn(word)

    def generate_blue_clue(self, n, penalty, remaining_agents):
        if len(remaining_agents) == 1:
            potentials = self.embedding.model.most_similar(positive=remaining_agents, topn=10)
            for pot in potentials:
                if self.is_valid_clue(pot) and "_" not in pot:
                    return pot, remaining_agents

        pq = []


        for word_set in itertools.combinations(remaining_agents, n):
            highest_clues, score = self.get_highest_blue_clue(word_set, penalty)
            heapq.heappush(pq, (-1 * score, highest_clues, word_set))

        best_clues = []
        best_board_words_for_clue = []
        best_scores = []
        count = 0

        while pq:
            score, clues, word_set = heapq.heappop(pq)
            while clues in best_clues:
                score, clues, word_set = heapq.heappop(pq)

            if count >= 5:
                break
            
            best_clues.append(clues)
            best_scores.append(score)
            best_board_words_for_clue.append(word_set)

            count += 1

        for clue, words in zip(best_clues, best_board_words_for_clue): 
            if clue not in self.used_clues:
                self.used_clues.append(clue)
                return (clue, words)

    def get_highest_blue_clue(self, chosen_words, penalty=1.0):
        potential_clues = set()
        for word in chosen_words:
            nns = self.weighted_nn[word]
            potential_clues.update(nns)
        
        highest_scoring_clues = []
        highest_score = float("-inf")

        for clue in potential_clues:
            if not self.is_valid_clue(clue):
                continue
            blue_word_counts = []
            for blue_word in chosen_words:
                if clue in self.weighted_nn[blue_word]:
                    blue_word_counts.append(self.weighted_nn[blue_word][clue])
                else:
                    blue_word_counts.append(self.embedding.get_word_similarity(blue_word, clue))
            
            embedding_score = self.embedding.penalise(chosen_words, clue, self.red_words)
            score = sum(blue_word_counts) + embedding_score

            # print(clue, len(blue_word_counts))
            
            if score > highest_score:
                highest_scoring_clues = [clue]
                highest_score = score
            elif score == highest_score:
                highest_scoring_clues.append(clue)
        
        return highest_scoring_clues, highest_score

    def generate_red_clue(self, n, penalty, remaining_agents):
        if len(remaining_agents) == 1:
            potentials = self.embedding.model.most_similar(positive=remaining_agents, topn=10)
            for pot in potentials:
                if self.is_valid_clue(pot) and "_" not in pot:
                    return pot, remaining_agents
            
        pq = []

        for word_set in itertools.combinations(remaining_agents, n):
            highest_clues, score = self.get_highest_red_clue(word_set, penalty)
            heapq.heappush(pq, (-1 * score, highest_clues, word_set))

        best_clues = []
        best_board_words_for_clue = []
        best_scores = []
        count = 0

        while pq:
            score, clues, word_set = heapq.heappop(pq)
            while clues in best_clues:
                score, clues, word_set = heapq.heappop(pq)

            if count >= 5:
                break
            
            best_clues.append(clues)
            best_scores.append(score)
            best_board_words_for_clue.append(word_set)

            count += 1

        for clue, words in zip(best_clues, best_board_words_for_clue): 
            if clue not in self.used_clues:
                self.used_clues.append(clue)
                return (clue, words)


    def get_highest_red_clue(self, chosen_words, penalty=1.0):
        potential_clues = set()
        for word in chosen_words:
            nns = self.weighted_nn[word]
            potential_clues.update(nns)
        
        highest_scoring_clues = []
        highest_score = float("-inf")

        for clue in potential_clues:
            if not self.is_valid_clue(clue):
                continue
            red_word_counts = []
            for red_word in chosen_words:
                if clue in self.weighted_nn[red_word]:
                    red_word_counts.append(self.weighted_nn[red_word][clue])
                else:
                    red_word_counts.append(self.embedding.get_word_similarity(red_word, clue))
            
            embedding_score = self.embedding.penalise(chosen_words, clue, self.blue_words)
            score = sum(red_word_counts) + embedding_score

            if score > highest_score:

                highest_scoring_clues = [clue]
                highest_score = score
            elif score == highest_score:
                highest_scoring_clues.append(clue)
        
        return highest_scoring_clues, highest_score

    def is_valid_clue(self, clue):
        for board_word in self.words:
            if (clue in board_word or board_word in clue or self.stemmer.stem(clue) == self.stemmer.stem(board_word) or not clue.isalpha()):
                return False
        return True

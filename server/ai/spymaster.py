class Spymaster:
    def __init__(self, id, red_clues, blue_clues):
        self.id = id
        self.red_clues = red_clues
        self.blue_clues = blue_clues
        self.red_used = []
        self.blue_used = []

    def generate_red_clue(self, remaining_agents):
        # first try get doubles
        for words, clues in self.red_clues.items():
            if words[0] in remaining_agents and words[1] in remaining_agents:
                for clue in clues:
                    if clue not in self.red_used:
                        self.red_used.append(clue)
                        return (f"{clue} {len(words)}", words)

        # otherwise just go for ones whether one is still there
        for words, clues in self.red_clues.items():
            if words[0] in remaining_agents or words[1] in remaining_agents:
                for clue in clues:
                    if clue not in self.red_used:
                        self.red_used.append(clue)
                        return (f"{clue} {len(words)}", words) 
            
    def generate_blue_clue(self, remaining_agents):
        # first try get doubles
        for words, clues in self.blue_clues.items():
            if words[0] in remaining_agents and words[1] in remaining_agents:
                for clue in clues:
                    if clue not in self.blue_used:
                        self.blue_used.append(clue)
                        return (f"{clue} {len(words)}", words) 

        # otherwise just go for ones whether one is still there
        for words, clues in self.blue_clues.items():
            if words[0] in remaining_agents or words[1] in remaining_agents:
                for clue in clues:
                    if clue not in self.blue_used:
                        self.blue_used.append(clue)
                        return (f"{clue} {len(words)}", words) 
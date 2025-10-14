from letters import Letter
import numpy as np

LETTERS_PER_RACK = 7


class Bag:

    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
        self.vowels = ["A", "E", "I", "O", "U", "Y", "?"]
        self.consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W",
                           "X", "Y", "Z", "?"]
        self.values = np.array([1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 10, 1, 2, 1, 1, 3, 8, 1, 1, 1, 1, 4, 10, 10, 10, 10, 0])
        self.repartition = np.array([9, 2, 2, 3, 15, 2, 2, 2, 8, 1, 1, 5, 3, 6, 6, 2, 1, 6, 6, 6, 6, 2, 1, 1, 1, 1, 2])
        self.letters = [Letter(self.alphabet[i], self.values[i], self.repartition[i]) for i in range(27)]

    def discard_rack(self, rack):
        count_vowels = sum([1 for char in ''.join(rack) if char in self.vowels])
        count_consonants = sum([1 for char in ''.join(rack) if char in self.consonants])
        if count_vowels < 2 or count_consonants < 2:
            return True
        else:
            return False

    def draw(self, leave):
        new_rack = ''.join(np.random.choice(list(self.alphabet),
                                            p=self.repartition / np.sum(self.repartition),
                                            size=LETTERS_PER_RACK - len(leave))) + leave
        if self.discard_rack(new_rack):
            return self.draw("")
        else:
            return ''.join(sorted(new_rack))


bag = Bag()

print(bag.draw(""))

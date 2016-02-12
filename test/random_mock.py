from board import BLUE_TEAM
from wordlist import word_list

class RandomMock:
    def __init__(self):
        self.choice_index = 0
        
    def choice(self, a_list):
        if len(a_list) == 2:
            return BLUE_TEAM
        else:
            self.choice_index += 1
            return word_list[self.choice_index]
        
    def shuffle(self, a_list):
        pass
import random

class Hangman:
    HANGMANPICS = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========''']

    def __init__(self, word_list):
        self.word_list = word_list
        self.word_to_guess = ""
        self.guessed_letters = []
        self.mistakes = 0
        self.max_mistakes = len(self.HANGMANPICS) - 1
        self.hide_words = []
        self.score = 0

    def start(self):
        self.word_to_guess = random.choice(self.word_list).upper()
        self.guessed_letters = []
        self.mistakes = 0
        self.hide_words = ["_"] * len(self.word_to_guess)
    def guess(self, letter):
        if letter == "!":
            return "Game exited by player"

        letter = letter.upper()
        if letter in self.guessed_letters:
            return "already guessed"

        self.guessed_letters.append(letter)
        if letter in self.word_to_guess:
            new_correct_guesses = []
            for i in range(len(self.word_to_guess)):
                if self.word_to_guess[i] == letter:
                    new_correct_guesses.append(letter)
                    self.score += 10
                else:
                    new_correct_guesses.append(self.hide_words[i])
            self.hide_words = new_correct_guesses
            return "correct"
        else:
            self.mistakes += 1
            return "incorrect"

    def get_status(self):
        hangman_pic_index = min(self.mistakes, self.max_mistakes)
        return {
            "word_to_guess": self.word_to_guess,
            "guessed_letters": self.guessed_letters,
            "mistakes": self.mistakes,
            "max_mistakes": self.max_mistakes,
            "hide_words": self.hide_words,
            "hangman_pic": self.HANGMANPICS[hangman_pic_index],
            "score": self.score
        }

    def is_game_over(self):
        if self.mistakes >= self.max_mistakes:
            return True
        if "_" not in self.hide_words:
            return True
        return False

    def get_result(self):
        if "_" not in self.hide_words:
            return "win"
        return "lose"
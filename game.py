import pandas as pd
from classes_game import Hangman

def start_game():

    df = pd.read_csv("words.csv")

    words_list = df.iloc[:, 0].tolist()
    game = Hangman(words_list)
    game.start()

    while not game.is_game_over():
        status = game.get_status()
        print(status["hangman_pic"])
        print(status["hide_words"])
        print(status["guessed_letters"])
        print("Mistakes",status["mistakes"],"/",status["max_mistakes"])
        letter = input("Guess a letter (or enter '!' to exit): ")
        print(game.guess(letter))
        if letter == "!":
            return 0


    if game.is_game_over():
        status = game.get_status()
        print(status["hangman_pic"])
        print(status["hide_words"])
        print("Mistakes",status["mistakes"],"/",status["max_mistakes"])
        print("Game Over! The word was:", status["word_to_guess"])
        print("You", game.get_result())
        if game.get_result() == "win":
            return status["score"]


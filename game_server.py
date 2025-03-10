import socket
import threading
import pandas as pd
from classes_game import Hangman

HOST = '127.0.0.1'
PORT = 65433

df = pd.read_csv("words.csv")
words_list = df.iloc[:, 0].tolist()
game = Hangman(words_list)
game.start()

def handle_client(conn):
    global game
    while not game.is_game_over():
        status = game.get_status()
        game_data = f"{' '.join(status['hide_words'])}|{','.join(status['guessed_letters'])}|{status['mistakes']}|{status['max_mistakes']}"
        conn.sendall(game_data.encode())

        letter = conn.recv(1024).decode().strip()
        if not letter:
            break

        print(f"Solver hádá: {letter}")
        game.guess(letter)

    final_status = game.get_status()
    conn.sendall(f"END|{final_status['word_to_guess']}".encode())
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("🟢 Server běží, čekám na solver...")

while True:
    conn, addr = server.accept()
    print(f"🔗 Solver připojen: {addr}")
    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()

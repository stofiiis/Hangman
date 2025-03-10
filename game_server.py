import socket
import threading
import pandas as pd
from classes_game import Hangman  # Import herní logiky

# 🔧 Nastavení serveru
HOST = '127.0.0.1'  # Lokální počítač
PORT = 65432  # Port pro komunikaci

# 📜 Načtení slovníku
df = pd.read_csv("words.csv")
words_list = df.iloc[:, 0].tolist()

# 🎮 Vytvoření nové hry
game = Hangman(words_list)
game.start()


def handle_client(conn):
    """ Komunikace se solverem: posílá stav hry, přijímá hádaná písmena """
    global game
    while not game.is_game_over():
        status = game.get_status()

        # 📡 Poslání aktuálního stavu solveru
        game_data = f"{' '.join(status['hide_words'])}|{','.join(status['guessed_letters'])}|{status['mistakes']}|{status['max_mistakes']}"
        conn.sendall(game_data.encode())

        # ⏳ Přijetí hádaného písmene od solveru
        letter = conn.recv(1024).decode().strip()
        if not letter:
            break

        print(f"Solver hádá: {letter}")
        game.guess(letter)

    # 🎯 Hra skončila, poslat výsledek
    final_status = game.get_status()
    conn.sendall(f"END|{final_status['word_to_guess']}".encode())
    conn.close()


# 🚀 Spuštění serveru
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("🔵 Hra Šibenice běží! Čekám na solver...")

while True:
    conn, addr = server.accept()
    print(f"🔗 Spojeno se solverem {addr}")
    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()

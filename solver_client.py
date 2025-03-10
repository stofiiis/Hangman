import socket
from collections import Counter
import pandas as pd

HOST = '127.0.0.1'  # Lokální IP adresa (musí odpovídat serveru)
PORT = 65432  # Port pro komunikaci

# 📜 Načtení slovníku
df = pd.read_csv("words.csv")
words_list = [word.upper() for word in df.iloc[:, 0].tolist()]


def filter_words_by_state(words, word_state, guessed_letters):
    """ Filtrování slov podle aktuálního stavu hádaného slova. """
    filtered_words = []
    for word in words:
        if len(word) != len(word_state):
            continue  # Vynecháme slova nesprávné délky

        match = True
        for i, letter in enumerate(word_state):
            if letter != "_" and word[i] != letter:  # Písmeno musí být na správném místě
                match = False
                break
            if letter == "_" and word[i] in guessed_letters:  # Vynecháme slova s už špatně hádanými písmeny
                match = False
                break

        if match:
            filtered_words.append(word)

    return filtered_words


def get_best_letter(words, guessed_letters):
    """ 📊 Najde nejčastější nepoužité písmeno v možných slovech. """
    letter_counts = Counter(letter for word in words for letter in word if letter not in guessed_letters)
    return letter_counts.most_common(1)[0][0] if letter_counts else None


# 🔗 Připojení k serveru (hře)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("🔴 Solver připojen k hře! Začínám hádat...")

while True:
    # 📡 Přijetí stavu hry
    data = client.recv(1024).decode().strip()

    if data.startswith("END"):
        print(f"🎉 Slovo bylo: {data.split('|')[1]}")
        break

    # 📦 Rozdělení přijatých dat
    word_state, guessed_letters, mistakes, max_mistakes = data.split('|')
    word_state = word_state.split(' ')
    guessed_letters = set(guessed_letters.split(',')) if guessed_letters else set()

    print(f"\n🟡 Aktuální stav hry: {' '.join(word_state)}")
    print(f"❌ Špatná písmena: {guessed_letters}")
    print(f"⚠️ Chyby: {mistakes} / {max_mistakes}")

    # ✅ Pokud je slovo kompletní, ukončíme
    if "_" not in word_state:
        print("🎯 Slovo je kompletní!")
        break

    # 🔎 Filtrování možných slov podle skrytého slova
    possible_words = filter_words_by_state(words_list, word_state, guessed_letters)
    if not possible_words:
        print("❌ Žádná vhodná slova nenalezena. Hádání končí.")
        break

    # 🔠 Vybrání nejlepšího písmena
    best_guess = get_best_letter(possible_words, guessed_letters)
    if not best_guess:
        print("❌ Žádná vhodná písmena k hádání. Hádání končí.")
        break

    print(f"🤖 Solver hádá písmeno: {best_guess}")
    client.sendall(best_guess.encode())

print("🔴 Solver ukončen.")
client.close()

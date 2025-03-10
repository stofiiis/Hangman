import bcrypt
import subprocess
import time
from DB_classes import db
from game import start_game

def name():
    while True:
        name_input = input("Enter your name: ").strip()
        if len(name_input) > 0:
            return name_input
        else:
            print("❌ Musíš zadat jméno!")

def password():
    while True:
        password_input = input("Enter your password: ").strip()
        if len(password_input) > 6:
            return password_input
        else:
            print("❌ Heslo musí mít alespoň 6 znaků!")

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def start_server():
    """ Spustí herní server na pozadí a čeká na solver """
    print("🟢 Spouštím server...")
    server_process = subprocess.Popen(["python", "game_server.py"])
    time.sleep(2)  # Krátká pauza, aby server mohl naběhnout
    return server_process

def game_menu(user_name):
    while True:
        print(f"\n🎮 Herní menu – Přihlášen jako: {user_name}")
        print("1. Start Game")
        print("2. View Score")
        print("3. Logout")

        game_input = input("Zadej volbu: ")
        if game_input == "1":
            server = start_server()  # Spustí server při startu hry
            print("🎲 Začínám hru...")
            score_new = start_game()
            server.terminate()  # Po skončení hry ukončí server

            if score_new is None:
                score_new = 0

            user = DB.get_user(user_name)[0]
            score_old = user[3]
            total_score = score_old + score_new
            DB.update_score(user_name, total_score)

            print(f"🏆 Získal jsi {score_new} bodů v této hře.")
            print(f"📊 Celkové skóre: {total_score}")

        elif game_input == "2":
            print("📜 Nejlepší hráči:")
            display_menu()

        elif game_input == "3":
            print("👋 Odhlášení...")
            return
        else:
            print("❌ Neplatná volba!")

def display_menu():
    top_users = DB.get_top_users()
    print("🏅 TOP 10 hráčů:")
    for i, user in enumerate(top_users, start=1):
        print(f"{i}. {user[0]} – {user[1]} bodů")

# Připojení k databázi
DB = db()
DB.c_execute('''CREATE TABLE IF NOT EXISTS users_score
                 (id INTEGER PRIMARY KEY, name TEXT, password TEXT, score INTEGER)''')

while True:
    print("\n🔑 Hlavní menu:")
    print("1. Registrace")
    print("2. Přihlášení")
    print("3. Ukončit")

    menu_option = input("Zadej volbu: ")

    if menu_option == "1":
        user_name = name()
        user_password = password()
        hashed_password = hash_password(user_password)
        DB.insert_user(user_name, hashed_password, 0)
        game_menu(user_name)

    elif menu_option == "2":
        while True:
            user_name = name()
            result = DB.get_user(user_name)

            if not result:
                print("❌ Uživatel nenalezen.")
            else:
                stored_password = result[0][2]
                user_password = password()

                if bcrypt.checkpw(user_password.encode('utf-8'), stored_password):
                    game_menu(user_name)
                    break
                else:
                    print("❌ Špatné heslo!")

    elif menu_option == "3":
        print("👋 Ukončuji program...")
        break

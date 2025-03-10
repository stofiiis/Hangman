import bcrypt
from DB_classes import db
from game import start_game

def name():
    while True:
        name_input = input("Enter your name: ")

        if len(name_input) > 0:
            return name_input
        else:
            print("Sorry, you didn't enter a name")
def password():
    while True:
        password_input = input("Enter your password: ")
        if len(password_input) > 6:
            return password_input
        else:
            print("Sorry, your password is too short")

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def menu():
    print("1. register")
    print("2. login")
    print("3. exit")

    while True:
        menu_input = input("Enter some number: ")
        if menu_input == "1":
            return menu_input
        elif menu_input == "2":
            return menu_input
        elif menu_input == "3":
            return menu_input
        else:
            print("Sorry, you didn't enter a number")



def game_menu(user_name):
    while True:
        print(f"Welcome to the game menu, {user_name}!")
        print("1. Start Game")
        print("2. View Score")
        print("3. Logout")

        game_input = input("Enter a number: ")
        if game_input == "1":
            print("Starting game...")
            score_new = start_game()
            if score_new is None:
                score_new = 0
            user = DB.get_user(user_name)[0]
            score_old = user[3]
            total_score = score_old + score_new
            DB.update_score(user_name, total_score)
            print(f"You have scored {score_new} points in this game.")
            print(f"Your total score is now {total_score}")
        elif game_input == "2":
            print("Displaying score...")
            display_menu()
        elif game_input == "3":
            print("Logging out...")
            return
        else:
            print("Invalid input, please try again.")

def display_menu():
    top_users = DB.get_top_users()
    i = 1
    print("Top 10 users by score:")
    for user in top_users:
        print(f"{i}. Name: {user[0]}, Score: {user[1]}")
        i += 1

DB = db()
DB.c_execute('''CREATE TABLE IF NOT EXISTS users_score
                 (id INTEGER PRIMARY KEY, name TEXT, password TEXT, score INTEGER)''')
while True:
    menu_option = menu()
    if menu_option == "1":




        user_name = name()

        user_password = password()
        hashed_password = hash_password(user_password)

        DB.insert_user(user_name, hashed_password, 0)
        game_menu(user_name)

    if menu_option == "2":
        while True:
            user_name = name()
            result = DB.get_user(user_name)
            if not result:
                print("User not found.")
            else:
                stored_password = result[0][2]

                user_password = password()
                if bcrypt.checkpw(user_password.encode('utf-8'), stored_password):
                    game_menu(user_name)
                    break
                else:
                    print("Sorry, incorrect password. Try again.")
    if menu_option == "3":
        print("Goodbye!")
        break






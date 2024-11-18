from threading import Thread
from queue import Queue
from art import tprint
from csv import DictReader, DictWriter

from gameLoop import GameLoop
from input import listen_input
from render import render_game
from helpers import clear_screen
from configs import select_config
from settings import settings

def main():
    text = settings.get_game_text("main_menu")
    lang = settings.get_game_text("language")

    while True:
        clear_screen()

        if settings.get_game_language() != lang:
            text = settings.get_game_text("main_menu")

        tprint("Pybrinha")

        print(text["start_opt"])
        print(text["leader_opt"])
        print(text["conf_opt"])
        print(text["leave_opt"])

        user_input = input(text["input_ask"])

        match user_input:
            case "1":
                run_game()
            case "2":
                leaderboard()
            case "3":
                config()
            case "4":
                tprint(text["goodbye"])
                exit()


def leaderboard():
    text = settings.get_game_text("leaderboard")

    clear_screen()
    tprint(text["greet"])

    with open("./data/leaderboard.csv") as file:
        data = list(DictReader(file))

        if data == []:
            print(f"{text["no_score"]}\n")
            input(text["press_continue"])
            return


        leaderboard = sorted(data, key=lambda row: int(row["score"]), reverse=True)
        for i, row in enumerate(leaderboard, start=1):
            print(f"{i:>2}.  {row["name"]:<6} {int(row['score']):010d}")

        input(f"\n{text["press_continue"]}")

def config():
    text = settings.get_game_text("configs_menu")
    lang = settings.get_game_text("language")

    while True:
        clear_screen()

        if settings.get_game_language() != lang:
            text = settings.get_game_text("configs_menu")

        tprint(text["greet"])

        print(text["difficulty_opt"])
        print(text["grid_opt"])
        print(text["lang_opt"])
        print(text["leader_opt"])
        print(text["leave_opt"])

        user_input = input(text["input_ask"])

        if select_config(user_input):
            break

def run_game():
    input_q = Queue(1)
    render_q = Queue(1)
    shutdown_q = Queue(1)

    keyboard_thread = Thread(target=listen_input, args=[input_q, shutdown_q])
    render_thread = Thread(target=render_game, args=[render_q, shutdown_q])
    game_thread = Thread(target=GameLoop, args=[render_q, input_q, shutdown_q])

    keyboard_thread.start()
    render_thread.start()
    game_thread.start()

    keyboard_thread.join()
    render_thread.join()
    game_thread.join()

    game_over(shutdown_q.get() * 100)

def game_over(score):
    text = settings.get_game_text("game_over")

    while True:
        clear_screen()

        tprint(text["greet"])
        print(f"{text["score"]}: {score:010d}\n")
        print(f"1. {text["try_again_opt"]}")
        print(f"2. {text["save_score_opt"]}")
        print(f"3. {text["go_menu_opt"]}")

        user_input = input(f"{text["input_ask"]}")

        match user_input:
            case "1":
                run_game()
                break
            case "2":
                save_score(score)
                break
            case "3":
                break

def save_score(score: int):
    text = settings.get_game_text("game_over")

    clear_screen()
    tprint(text["greet"])
    initials = input(text["ask_initials"]).strip().upper()

    while len(initials) != 3 or not initials.isalpha():
        clear_screen()
        tprint(text["greet"])

        print(f"{text["invalid_initials"]}\n")
        initials = input(text["ask_initials"]).strip().upper()

    with open("./data/leaderboard.csv", 'a', newline='') as file:
        writer = DictWriter(file, fieldnames=["name", "score"])
        writer.writerow({"name": initials, "score": score})

    clear_screen()
    tprint(text["greet"])

    print(f"{text["score_sucess"]}\n")
    input(text["wait_msg"])

main()



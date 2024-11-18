from threading import Thread
from queue import Queue
from art import tprint

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
    pass

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
    text = settings.get_game_text("configs_menu")
    while True:
        clear_screen()

        tprint("Game over")
        print(f"Final Score: {score:010d}\n")
        print("1. Try Again")
        print("2. Save Score")
        print("3. Go to main menu")

        user_input = input(f"{text["input_ask"]}")

        match user_input:
            case "1":
                run_game()
                break
            case "2":
                save_score()
                break
            case "3":
                break

def save_score():
    pass

main()



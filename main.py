from threading import Thread
from queue import Queue
from art import tprint

from input import listen_input
from state import game_state
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
                break


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
    state_q = Queue(1)

    state_q.put(settings.get_game_grid())

    t1 = Thread(target=listen_input, args=[input_q])
    t2 = Thread(target=render_game, args=[state_q])
    t3 = Thread(target=game_state, args=[state_q, input_q])

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

main()

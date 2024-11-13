from settings import settings
from helpers import clear_screen
from art import tprint

def select_config(user_input: str) -> bool:
    match user_input:
        case "1":
            change_difficulty()
        case "2":
            change_grid_size()
        case "3":
            change_language()
        case "4":
            clear_leaderboard()
        case "5":
            return True

    return False

def change_difficulty():
    text_difficulties = settings.get_game_text("difficulty")
    text_configs = settings.get_game_text("configs_menu")
    difficulties = settings.get_difficulties().items()

    while True:
        clear_screen()
        tprint(text_configs["greet_difficulty"])

        for i, difficulty in enumerate(difficulties, start=1):
            if (difficulty[1] == settings.get_game_difficulty()):
                print(f"{i}. {text_difficulties[difficulty[0]]:10} [X]")
            else:
                print(f"{i}. {text_difficulties[difficulty[0]]:10} [ ]")

        print(f"{len(difficulties) + 1}. {text_configs["goback_opt"]}")

        try:
            user_input = int(input(text_configs["input_ask"]))
        except ValueError:
            continue

        if user_input == len(difficulties) + 1:
            break
        elif user_input > len(difficulties) or user_input <= 0:
            continue
        else:
            settings.set_game_difficulty(list(difficulties)[user_input - 1][0])

def change_grid_size():
    text_grids = settings.get_game_text("grid")
    text_configs = settings.get_game_text("configs_menu")
    grids = settings.get_grid_sizes().items()

    while True:
        clear_screen()
        tprint(text_configs["greet_grid"])

        for i, grid in enumerate(grids, start=1):
            if (grid[1] == settings.get_game_grid_len()):
                print(f"{i}. {text_grids[grid[0]]:10} [X]")
            else:
                print(f"{i}. {text_grids[grid[0]]:10} [ ]")

        print(f"{len(grids) + 1}. {text_configs["goback_opt"]}")

        try:
            user_input = int(input(text_configs["input_ask"]))
        except ValueError:
            continue

        if user_input == len(grids) + 1:
            break
        elif user_input > len(grids) or user_input <= 0:
            continue
        else:
            settings.set_game_grid(list(grids)[user_input - 1][0])

def change_language():
    text_languages = settings.get_game_text("languages")
    text_configs = settings.get_game_text("configs_menu")

    while True:
        clear_screen()

        tprint(text_configs["greet_language"])

        for i, language in enumerate(text_languages.items(), start=1):
            if language[0] == settings.get_game_language():
                print(f"{i}. {language[1]:20} [X]")
            else:
                print(f"{i}. {language[1]:20} [ ]")

        print(f"{len(text_languages) + 1}. {text_configs["goback_opt"]}")

        try:
            user_input = int(input(text_configs["input_ask"]))
        except ValueError:
            continue

        if user_input == len(text_languages) + 1:
            break
        elif user_input > len(text_languages) or user_input <= 0:
            continue
        else:
            settings.set_game_text_language(list(text_languages.keys())[user_input - 1])

def clear_leaderboard():
    text_configs = settings.get_game_text("configs_menu")
    while True:

        clear_screen()

        tprint(text_configs["greet"])

        print(text_configs["leader_conf"])
        print(text_configs["leader_yes"])
        print(text_configs["leader_no"])

        user_input = input(text_configs["input_ask"])

        if user_input == "1":
            stop_and_wait(text_configs["leader_msg"])
            break
        elif user_input == "2":
            break

def stop_and_wait(message):
    text_configs = settings.get_game_text("configs_menu")

    clear_screen()
    print(message + "\n")
    print(text_configs["wait_msg"])

    input()

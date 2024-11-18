from art import tprint
from helpers import clear_screen
from settings import settings
from copy import deepcopy
from queue import Queue
from collections import deque
from random import randint
from time import sleep
from typing import Literal
from gameTypes import SnakeCoordinates, GameGrid, TailClash, OutOfBonds

class GameLoop:

    def __init__(self, render_queue: Queue, controls_queue: Queue, shutdown_queue: Queue):
        self.__render_queue = render_queue
        self.__controls_queue = controls_queue
        self.__shutdown_queue = shutdown_queue

        self.__current_difficulty: int = settings.get_game_difficulty()
        self.__current_score: int = 0
        self.__current_grid: GameGrid = deepcopy(settings.get_game_grid())

        self.__grid_size_y: int = len(self.__current_grid)
        self.__grid_size_x: int = len(self.__current_grid[0])

        self.__snake_head_coordinates: SnakeCoordinates = {
            "x": self.__grid_size_x // 2,
            "y": self.__grid_size_y // 2,
        }

        self.__snake_coordinates_queue = deque()
        self.__append_snake_coordinates_to_queue()

        self.__snake_size = 2

        self.__game_text = settings.get_game_text("game_loop")

        self.__start()

    def __start(self):
        self.__update_snake_head("v")
        self.__render_queue.put({
            "score": self.__current_score,
            "grid": self.__current_grid,
        })

        current_input: str = self.__controls_queue.get()
        self.__generate_fruit()

        while True:
            sleep(0.1 * (self.__current_difficulty - self.__current_score // 50))

            if not self.__controls_queue.empty():
                current_input = self.__controls_queue.get()

            if self.__snake_size <= len(self.__snake_coordinates_queue):
                self.__update_snake_tail()

            try:
                match current_input:
                    case "u":
                        self.__update_snake_position("y", -1, "ʌ")
                    case "d":
                        self.__update_snake_position("y",  1, "v")
                    case "l":
                        self.__update_snake_position("x", -1, "<")
                    case "r":
                        self.__update_snake_position("x",  1, ">")
                    case -1:
                        self.__stop_game(self.__game_text["giving_up"])
                        return

            except TailClash:
                self.__update_snake_head("X")
                self.__render_queue.put({
                    "score": self.__current_score,
                    "grid": self.__current_grid,
                })

                self.__stop_game(self.__game_text["eating_tail"])
                return
            except OutOfBonds:
                self.__snake_head_coordinates = self.__snake_coordinates_queue.pop()
                self.__update_snake_head("X")
                self.__render_queue.put({
                    "score": self.__current_score,
                    "grid": self.__current_grid,
                })

                self.__stop_game(self.__game_text["hitting_wall"])
                return
            except:
                self.__stop_game(self.__game_text["random_bug"])
                return

    def __stop_game(self, message: str):
        sleep(0.25)
        self.__shutdown_queue.put(self.__current_score)
        sleep(0.25)

        clear_screen()
        tprint(self.__game_text["game_over_greet"])
        print(f"\n{message}")
        print(f"\n{self.__game_text["wait_msg"]}")

    def __update_snake_position(self, axis: Literal["x", "y"], move_step: int, head_character: str):
        self.__update_snake_head("o")
        self.__append_snake_coordinates_to_queue()

        self.__snake_head_coordinates[axis] += move_step

        if self.__tile_is_out_of_bounds(axis):
            raise OutOfBonds("")

        head = self.__snake_head_coordinates

        if self.__tile_is_snake(head["x"], head["y"]):
            raise TailClash()

        if self.__tile_have_fruit(head["x"], head["y"]):
            self.__snake_size += 1
            self.__current_score += 1
            self.__generate_fruit()

        self.__update_snake_head(head_character)

        self.__render_queue.put(
            {
                "score": self.__current_score,
                "grid": self.__current_grid,
            })

    def __tile_is_out_of_bounds(self, axis: Literal["x", "y"]) -> bool:
        if axis == "x":
            max_size = self.__grid_size_x
        else:
            max_size = self.__grid_size_y

        if self.__snake_head_coordinates[axis] >= max_size:
            return True
        elif self.__snake_head_coordinates[axis] < 0:
            return True
        else:
            return False

    def __append_snake_coordinates_to_queue(self):
        self.__snake_coordinates_queue.append(self.__snake_head_coordinates.copy())

    def __update_snake_head(self, char: str):
        head = self.__snake_head_coordinates

        self.__current_grid[head["y"]][head["x"]] = char

    def __update_snake_tail(self):
        tail = self.__snake_coordinates_queue.popleft()

        self.__current_grid[tail["y"]][tail["x"]] = " "

    def __generate_fruit(self):
        rand_x = randint(0, self.__grid_size_x - 1)
        rand_y = randint(0, self.__grid_size_y - 1)

        if self.__tile_is_busy(rand_x, rand_y):
            self.__generate_fruit()
        else:
            self.__current_grid[rand_y][rand_x] = "@"

    def __tile_is_busy(self, tile_x, tile_y) -> bool:
        if self.__current_grid[tile_y][tile_x] == " ":
            return False
        else:
            return True

    def __tile_is_snake(self, tile_x, tile_y) -> bool:
        if self.__current_grid[tile_y][tile_x] == "o":
            return True
        else:
            return False

    def __tile_have_fruit(self, tile_x, tile_y) -> bool:
        if self.__current_grid[tile_y][tile_x] == "@":
            return True
        else:
            return False

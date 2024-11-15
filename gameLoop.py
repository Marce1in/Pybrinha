from settings import settings
from queue import Queue
from random import randint
from time import sleep
from typing import Literal
from gameTypes import SnakeCoordinates, GameGrid

class GameLoop:

    def __init__(self, render_queue: Queue, controls_queue: Queue):
        self.__render_queue = render_queue
        self.__controls_queue = controls_queue

        self.__current_grid: GameGrid = settings.get_game_grid()

        self.__grid_size_y: int = len(self.__current_grid)
        self.__grid_size_x: int = len(self.__current_grid[0])

        self.__snake_head_coordinates: SnakeCoordinates = {
            "x": self.__grid_size_x // 2,
            "y": self.__grid_size_y // 2,
        }

        self.__snake_coordinates_queue = Queue()
        self.__append_snake_coordinates_to_queue()

        self.__snake_size = 2

        self.__start()

    def __start(self):
        self.__update_snake_head("v")
        self.__render_queue.put(self.__current_grid)

        current_input: int = self.__controls_queue.get()
        self.__generate_fruit()

        while True:
            sleep(0.1 * settings.get_game_difficulty())

            if not self.__controls_queue.empty():
                current_input = self.__controls_queue.get()

            if self.__snake_size <= self.__snake_coordinates_queue.qsize():
                self.__update_snake_tail()

            try:
                match current_input:
                    case "u":
                        self.__update_snake_position("y", -1, "ʌ")
                    case "d":
                        self.__update_snake_position("y", 1, "v")
                    case "l":
                        self.__update_snake_position("x", -1, "<")
                    case "r":
                        self.__update_snake_position("x", 1, ">")
            except:
                break



    def __update_snake_position(self, axis: Literal["x", "y"], move_step: int, head_character: str):
        self.__update_snake_head("o")
        self.__append_snake_coordinates_to_queue()

        if self.__tile_is_out_of_bounds(axis, move_step):
            raise Exception("Snake out of array bounds")

        self.__snake_head_coordinates[axis] += move_step

        head_x = self.__snake_head_coordinates["x"]
        head_y = self.__snake_head_coordinates["y"]

        if self.__tile_have_fruit(head_x, head_y):
            self.__snake_size += 1
            self.__generate_fruit()

        if self.__tile_is_snake(head_x, head_y):
            raise Exception("Snake eaten his own tail")

        self.__update_snake_head(head_character)
        self.__render_queue.put(self.__current_grid)

    def __tile_is_out_of_bounds(self, axis: Literal["x", "y"], move_step: int) -> bool:
        if axis == "x":
            max_size = self.__grid_size_x
        else:
            max_size = self.__grid_size_y

        if self.__snake_head_coordinates[axis] + move_step > max_size:
            return True
        elif self.__snake_head_coordinates[axis] <= 0:
            return True
        else:
            return False

    def __append_snake_coordinates_to_queue(self):
        self.__snake_coordinates_queue.put(self.__snake_head_coordinates.copy())

    def __update_snake_head(self, char: str):
        head_x = self.__snake_head_coordinates["x"]
        head_y = self.__snake_head_coordinates["y"]

        self.__current_grid[head_y][head_x] = char

    def __update_snake_tail(self):
        tail = self.__snake_coordinates_queue.get()

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

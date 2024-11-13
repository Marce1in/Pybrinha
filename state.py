from settings import settings
from gameTypes import SnakeCoordinates, GameGrid
import random
import queue
import time


def game_state(render_pipeline: queue.Queue, keys_pipeline: queue.Queue):
    game_difficulty: int = settings.get_game_difficulty()

    current_grid: GameGrid = render_pipeline.get()

    size_y: int = len(current_grid)
    size_x: int = len(current_grid[0])

    # Coordinates from where the snake head is in the game grid
    head: SnakeCoordinates = {
        "x": size_x // 2,
        "y": size_y // 2,
    }

    buffer: list[SnakeCoordinates] = [head]
    snake_size: int = 3

    update_head(current_grid, head, "v")
    render_pipeline.put(current_grid)

    input_current: int = keys_pipeline.get()
    generate_fruit(current_grid, size_x, size_y)

    while(True):
        time.sleep(0.1 * game_difficulty)

        if not keys_pipeline.empty():
            input_current = keys_pipeline.get()

        if not render_pipeline.empty():
            current_grid = render_pipeline.get()

        if snake_size <= len(buffer):
            update_tail(current_grid, buffer)


        match input_current:
            case 0:
                update_head(current_grid, head, "o")
                buffer.append(head.copy())

                head["y"] -= 1
                if (tile_have_fruit(current_grid, head)):
                    snake_size += 1
                    generate_fruit(current_grid, size_x, size_y)

                update_head(current_grid, head, "ʌ")
                render_pipeline.put(current_grid)
            case 1:
                update_head(current_grid, head, "o")
                buffer.append(head.copy())

                head["y"] += 1
                if (tile_have_fruit(current_grid, head)):
                    snake_size += 1
                    generate_fruit(current_grid, size_x, size_y)

                update_head(current_grid, head, "v")
                render_pipeline.put(current_grid)
            case 2:
                update_head(current_grid, head, "o")
                buffer.append(head.copy())

                head["x"] -= 1
                if (tile_have_fruit(current_grid, head)):
                    snake_size += 1
                    generate_fruit(current_grid, size_x, size_y)

                update_head(current_grid, head, "<")
                render_pipeline.put(current_grid)
            case 3:
                update_head(current_grid, head, "o")
                buffer.append(head.copy())

                head["x"] += 1
                if (tile_have_fruit(current_grid, head)):
                    snake_size += 1
                    generate_fruit(current_grid, size_x, size_y)

                update_head(current_grid, head, ">")
                render_pipeline.put(current_grid)

def update_head(state: GameGrid, head: SnakeCoordinates, char: str):
    state[head["y"]][head["x"]] = char

def update_tail(state: GameGrid, buffer: list[SnakeCoordinates]):
    tail = buffer.pop(0)
    state[tail["x"]][tail["y"]] = " "

def generate_fruit(state: GameGrid, size_x: int, size_y: int):
    rand_x = random.randint(0, size_x - 1)
    rand_y = random.randint(0, size_y - 1)

    if tile_is_busy(state, {"y": rand_y, "x": rand_x}):
        generate_fruit(state, size_x, size_y)
    else:
        state[rand_y][rand_x] = "@"

def tile_have_fruit(state: GameGrid, head: SnakeCoordinates) -> bool:
    if (state[head["y"]][head["x"]] == "@"):
        return True
    else:
        return False

def tile_is_busy(state: GameGrid, head: SnakeCoordinates) -> bool:
    if (state[head["y"]][head["x"]] == " "):
        return False
    else:
        return True

from typing import TypedDict

SnakeCoordinates = TypedDict("SnakeCoordinates", {"x": int, "y": int})

GameGrid = list[list[str]]

class OutOfBonds(Exception):
    pass

class TailClash(Exception):
    pass

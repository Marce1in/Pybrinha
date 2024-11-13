import tomllib

class Settings:

    def __init__(self):
        self.__language, self.__difficulty, self.__grid_size = self.__load_user_settings()

        self.__DIFFICULTIES = {
            "ign" : 0.2,
            "easy" : 0.5,
            "normal" : 1,
            "hard" : 2,
            "hell" : 3,
        }
        self.__GRID_SIZES = {
            "tiny" : 8,
            "small" : 16,
            "medium" : 32,
            "big" : 64,
            "huge" : 128,
        }

        self.__LANGUAGES = {"en", "br"}

        self.__game_text = self.__load_lang()
        self.__game_grid = self.__create_game_grid()
        self.__game_difficulty = self.__DIFFICULTIES[self.__difficulty]


    def __create_game_grid(self) -> list[list]:
        return [[" "] * self.__GRID_SIZES[self.__grid_size] for _ in range(self.__GRID_SIZES[self.__grid_size])]

    def __load_lang(self) -> dict:
        with open(f"./langs/{self.__language}.toml", "rb") as file:
            return tomllib.load(file)

    def __load_user_settings(self) -> tuple[str, str, str]:
        with open(f"./data/settings.toml", "rb") as file:
            data = tomllib.load(file)
            return data["language"], data["difficulty"], data["grid_size"]


    # Getters
    def get_game_text(self, subject=None) -> dict:
        if subject not in self.__game_text:
            raise Exception(f"This subject {subject} does not exist")
        else:
            return self.__game_text[subject]

    def get_game_grid(self) -> list[list]:
        return self.__game_grid

    def get_game_difficulty(self) -> int:
        return self.__game_difficulty

    def get_game_language(self) -> str:
        return self.__language

    def get_game_grid_len(self) -> int:
        return len(self.__game_grid)

    def get_difficulties(self) -> dict:
        return self.__DIFFICULTIES

    def get_grid_sizes(self) -> dict:
        return self.__GRID_SIZES


    # Setters
    def set_game_text_language(self, language: str):
        if(language not in self.__LANGUAGES):

            raise Exception(f"The language {language} is not supported")

        self.__language = language
        self.__update_game_text()

    def set_game_grid(self, grid_size: str):
        if(grid_size not in set(self.__GRID_SIZES.keys())):
            raise Exception(f"The grid size {grid_size} is not supported")

        self.__grid_size = grid_size
        self.__update_game_grid()

    def set_game_difficulty(self, difficulty: str):
        if(difficulty not in set(self.__DIFFICULTIES.keys())):
            raise Exception(f"The difficulty {difficulty} is not supported")

        self.__difficulty = difficulty
        self.__update_game_difficulty()


    # Updaters
    def __update_game_text(self):
        self.__game_text = self.__load_lang()

    def __update_game_grid(self):
        self.__game_grid = self.__create_game_grid()

    def __update_game_difficulty(self):
        self.__game_difficulty = self.__DIFFICULTIES[self.__difficulty]

settings = Settings()

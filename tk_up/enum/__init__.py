from enum import Enum

if __name__ == "__main__":
    print("init_enum")


class Scroll(Enum):
    X: str = "scroll_x"
    Y: str = "scroll_y"
    ALL: str = "scroll_all"
from pathlib import Path

from PIL import Image, ImageTk

class Wimage():

    i: ImageTk.PhotoImage
    name: str

    def __init__(self, path: str, size: tuple[int, int]) -> None:
        self.name = Path(path).stem
        temp = Image.open(path)
        temp = temp.resize(size, Image.LANCZOS)
        self.i = ImageTk.PhotoImage(temp, size=size)

    def get(self) -> ImageTk.PhotoImage:
        return self.i
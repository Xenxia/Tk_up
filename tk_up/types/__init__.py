from typing import Callable, TypeAlias, Tuple


Text: TypeAlias = str | tuple[Callable, tuple]
FuncsUpdate: TypeAlias = list[Callable]

Image: TypeAlias = Tuple[str, Tuple[int, int]]
Images: TypeAlias = list[Image]
ImageToggle: TypeAlias = Tuple[Image, Image]
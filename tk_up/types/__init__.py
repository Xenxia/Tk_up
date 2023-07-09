from typing import Callable, TypeAlias, Tuple


Text: TypeAlias = str | tuple[Callable, tuple]
FuncsUpdate: TypeAlias = list[Callable]
ImageToggle: TypeAlias = Tuple[Tuple[str, Tuple[int, int]], Tuple[str, Tuple[int, int]]]
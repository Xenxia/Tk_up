from typing import Callable, TypeAlias


Text: TypeAlias = str | tuple[Callable, tuple]
FuncsUpdate: TypeAlias = list[Callable]
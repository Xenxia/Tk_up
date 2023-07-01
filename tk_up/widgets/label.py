from typing import Callable, Any
from tkinter import ttk

from tk_up.widgets.w import Widget_up
from tk_up.types import Text

class Label_up(ttk.Label, Widget_up):

    textCall: tuple[Callable, list[Any]]
    textDynamic: bool

    def __init__(self, master=None, text: Text="" , **kw):

        ttk.Label.__init__(self, master=master, **kw)
        Widget_up.__init__(self)
        self.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.nametowidget('.').bind("<<TK_UP.Update>>", self.__update, add="+")

        self.textDynamic = False

        if isinstance(text, tuple):
            self.textDynamic = True
            self.textCall = text
            self.configure(text=f"{self.textCall[0](*self.textCall[1])}")

        elif isinstance(text, str):
            self.configure(text=text)

    def __update(self, event) -> None:
        if self.textDynamic:
            self.configure(text=f"{self.textCall[0](*self.textCall[1])}")
            self.update()


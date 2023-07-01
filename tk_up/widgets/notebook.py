from copy import copy
from tkinter import ttk

from tk_up.widgets.w import Widget_up
from tk_up.widgets.frame import Frame_up



class Tab_up(ttk.Notebook, Widget_up):

    tabs: dict[str, tuple[int, Frame_up]] = {}
    __num: int = 0

    def __init__(self, master=None, cursor=None) -> None:
        ttk.Notebook.__init__(self, master=master, cursor=cursor)
        Widget_up.__init__(self)

    def add_tab(self, name: str) -> Frame_up:

        frame = Frame_up(self)

        self.tabs[name] = copy((self.__num, copy(frame)))

        self.add(self.tabs[name][1], text=name)

        self.__num += 1

        return self.tabs[name][1]

    def get_tab(self, name: str) -> Frame_up:
        return self.tabs[name][1]

    def disable_tab(self, name: str):
        self.tab(self.tabs[name][0], state="disabled")

    def enable_tab(self, name: str):
        self.tab(self.tabs[name][0], state="normal")

    def del_tab(self, name: str):
        self.forget(self.tabs[name][0])

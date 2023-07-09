from typing import Callable, Any
from tkinter import ttk

from tk_up.widgets.w import Widget_up

class Label_up(ttk.Label, Widget_up):

    textCall: tuple[Callable, list[Any]]

    def __init__(self, master=None, **kw):

        ttk.Label.__init__(self, master=master, **kw)
        Widget_up.__init__(self)




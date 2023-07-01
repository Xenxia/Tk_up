from tkinter import ttk, StringVar, IntVar
from typing import Tuple

from tk_up.widgets.w import Widget_up



class OptionMenu_up(ttk.Combobox, Widget_up):

    def __init__(self, master=None, style=None, type: str="str", default: int=None, list: Tuple | list=None, **kw) -> None:

        type_var: StringVar | IntVar

        if type == "str":
            type_var = StringVar()
        elif type == "int":
            type_var = IntVar()

        ttk.Combobox.__init__(self, master, values=list ,textvariable=type_var, state="readonly", **kw)
        Widget_up.__init__(self)

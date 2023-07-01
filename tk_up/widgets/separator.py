from tkinter import ttk
from typing import Literal

from tk_up.widgets.w import Widget_up

class Separator_up(ttk.Separator, Widget_up):

    def __init__(self, master=None, cursor=None, name:str=None, orient:Literal["horizontal", "vertical"]="horizontal", style:str=None, takefocus=None) -> None:

        ttk.Separator.__init__(self, master=master, cursor=cursor, name=name, orient=orient, style=style, takefocus=takefocus)
        Widget_up.__init__(self)

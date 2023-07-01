
from tkinter import ttk, StringVar
from tkinter.constants import DISABLED, NORMAL
from typing import Any, Tuple
from PIL import Image, ImageTk

from tk_up.types import Text
from tk_up.widgets.w import Widget_up

class Button_up(ttk.Button, Widget_up):

    def __init__(self, master=None, text: Text="", image: str=None, **kw):

        self.i = None

        if image is not None:
            temp = Image.open(image)
            self.i = ImageTk.PhotoImage(temp)

        ttk.Button.__init__(self, master=master, image=self.i, **kw)
        Widget_up.__init__(self)
        self.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.nametowidget('.').bind("<<TK_UP.Update>>", self.__update, add="+")

        self.textDynamic = False

        if isinstance(text, tuple):
            self.textDynamic = True
            self.textCall = text
            t = text[0](*text[1])
            self.configure(text=t)
            
        elif isinstance(text, str):
            self.configure(text=text)

    def disable(self):
        self['state'] = DISABLED

    def enable(self):
        self['state'] = NORMAL

    def __update(self, event) -> None:
        if self.textDynamic:
            self.configure(text=f"{self.textCall[0](*self.textCall[1])}")
            self.update()

class Toggle_Button_up(Button_up):

    text: Tuple = ("ON", "OFF")
    style: Tuple = None
    status: bool
    func1: Any
    func2: Any

    def __init__(self, master=None, **kw):
        Button_up.__init__(self, master=master, **kw, command=self.toggle)
        self.status = True
        self.reload()
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.func1 = self.__
        self.func2 = self.__

    def __(self):
        pass

    def set_toggle_function(self, func1, func2):

        self.func1 = func1
        self.func2 = func2

    def reload(self):
        if self.status:
            self.config(text=self.text[0])
            if self.style is not None: self.config(style=self.style[0])
            self.status = True
        else:
            self.config(text=self.text[1])
            if self.style is not None: self.config(style=self.style[1])
            self.status = False

    def custom_toggle(self, text: Tuple = None, style: Tuple = None):
        if text is not None: self.text = text
        if style is not None: self.style = style
        self.reload()

    def set_default_status(self, status: bool):
        self.status = status
        self.reload()

    def get_status(self) -> bool:
        return self.status

    def set_status(self, status:bool, reload:bool = False):
        self.status = status

        if reload:
            self.reload()

    def toggle(self):
    
        if self.status:
            self.func1()
            self.config(text=self.text[1])
            if self.style is not None: self.config(style=self.style[1])
            self.status = False
        else:
            self.func2()
            self.config(text=self.text[0])
            if self.style is not None: self.config(style=self.style[0])
            self.status = True

class Checkbutton_up(ttk.Checkbutton, Widget_up):

    variable: StringVar

    def __init__(self, master=None, **kw):
        self.variable = StringVar()

        ttk.Checkbutton.__init__(self, master=master, variable=self.variable, onvalue=1, offvalue=0, **kw)
        Widget_up.__init__(self)

    def disable(self):
        self['state'] = DISABLED

    def enable(self):
        self['state'] = NORMAL

    def get(self):
        return self.variable

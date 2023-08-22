
from tkinter import ttk, StringVar
from typing import Any, Tuple
from PIL import Image, ImageTk

from tk_up.widgets.w import Widget_up, UpdateWidget, StateWidget
from tk_up.types import ImageToggle
from tk_up.object.image import Wimage

class Button_up(ttk.Button, Widget_up, UpdateWidget, StateWidget):

    def __init__(self, master=None, images: list[Wimage]=None, image: Wimage=None, **kw):

        ttk.Button.__init__(self, master=master, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)
        StateWidget.__init__(self)

        self.images = [None]
        self.image = None

        if image is not None:
            self.image = image
            self.config(image=self.image.get())

        if images is not None:
            self.images = images
            self.config(image=self.images[0].get())

        self.update()


    def set_image(self, name):

        for i in self.images:
            if i.name == name:
                self.config(image=i.get())
                break

        self.update()

class Toggle_Button_up(Button_up):

    text: Tuple = ("ON", "OFF")
    style: Tuple = None
    status: bool
    func1: Any
    func2: Any
    image1: ImageTk.PhotoImage
    image2: ImageTk.PhotoImage

    def __init__(self, master=None, **kw):
        Button_up.__init__(self, master=master, **kw, command=self.toggle)
        self.status = True
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.func1 = self.__
        self.func2 = self.__
        self.image1 = None
        self.image2 = None
        self.text = None
        self.reload()

    def __(self):
        pass

    def set_toggle_function(self, func1, func2):

        self.func1 = func1
        self.func2 = func2

    def reload(self):
        if self.status:
            if self.text is not None: self.config(text=self.text[0])
            if self.style is not None: self.config(style=self.style[0])
            if self.image1 is not None: self["image"] = self.image1
            self.status = True
        else:
            if self.text is not None: self.config(text=self.text[1])
            if self.style is not None: self.config(style=self.style[1])
            if self.image2 is not None: self["image"] = self.image2
            self.status = False

        self.update()

    def custom_toggle(self, text: Tuple = None, style: Tuple = None, image: ImageToggle = None):
        if text is not None: self.text = text
        if style is not None: self.style = style
        if image is not None:
            temp = Image.open(image[0][0])
            temp = temp.resize(image[0][1], Image.LANCZOS)
            self.image1 = ImageTk.PhotoImage(temp, size=image[0][1])

            temp = Image.open(image[1][0])
            temp = temp.resize(image[1][1], Image.LANCZOS)
            self.image2 = ImageTk.PhotoImage(temp, size=image[1][1])

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
            if self.text is not None: self.config(text=self.text[1])
            if self.style is not None: self.config(style=self.style[1])
            if self.image2 is not None: self["image"] = self.image2
            self.status = False
        else:
            self.func2()
            if self.text is not None: self.config(text=self.text[0])
            if self.style is not None: self.config(style=self.style[0])
            if self.image1 is not None: self["image"] = self.image1
            self.status = True

        self.update()

class Checkbutton_up(ttk.Checkbutton, Widget_up, UpdateWidget, StateWidget):

    variable: StringVar

    def __init__(self, master=None, **kw):
        self.variable = StringVar()

        ttk.Checkbutton.__init__(self, master=master, variable=self.variable, onvalue=1, offvalue=0, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)
        StateWidget.__init__(self)

    def get(self):
        return self.variable

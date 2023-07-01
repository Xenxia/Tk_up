import re as regex
from tkinter import Toplevel, ttk


class Toplevel_up(Toplevel, ttk.Frame):

    top: Toplevel
    # Size screen
    rootHeigth: int
    rootWidth: int

    def __init__(self, master=None, cnf={}, **kw):

        Toplevel.__init__(self, master=master, cnf=cnf, **kw)
        self.rootWidth = self.winfo_screenwidth()
        self.rootHeigth = self.winfo_screenheight()
        self.protocol("WM_DELETE_WINDOW", self.hide)

    def configWindows(self, title:str="Tk_Up", geometry:str="500x500", iconbitmap:str=None):

        if regex.findall(r"\+center", geometry) != []:
            gSizeW, gSizeH = geometry.split("+", 1)[0].split("x", 1)
            rootH = round((self.rootHeigth/2)-(int(gSizeH)/2))
            rootW = round((self.rootWidth/2)-(int(gSizeW)/2))
            geometry = f'{gSizeW}x{gSizeH}+{rootW}+{rootH}'

        self.title(title)
        self.geometry(geometry)
        if iconbitmap is not None:
            self.iconbitmap(iconbitmap)

        return self

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

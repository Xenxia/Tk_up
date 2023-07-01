from tkinter import ttk
from tkinter.constants import END

from tk_up.widgets.w import Widget_up

class Entry_up(ttk.Entry, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Entry.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

    def clear(self):
        self.delete(0, END)
        return self

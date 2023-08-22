from tkinter import ttk
from tkinter.constants import END

from tk_up.widgets.w import Widget_up, UpdateWidget, StateWidget

class Entry_up(ttk.Entry, Widget_up, UpdateWidget, StateWidget):

    limitChar: int

    def __init__(self, master=None, limitChar: int = 0, **kw):

        self.limitChar = limitChar

        ttk.Entry.__init__(self, master=master, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)
        StateWidget.__init__(self)

        self.bind("<KeyPress>", self.max)

    def clear(self):
        self.delete(0, END)
        return self
    
    def max(self, event):

        excludeKey = [8]

        if len(self.get()) >= self.limitChar and self.limitChar != 0 and self.limitChar > 0 and event.keycode not in excludeKey:
            return "break"

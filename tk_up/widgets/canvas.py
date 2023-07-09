from tkinter import Canvas

from tk_up.widgets.w import Widget_up, UpdateWidget

class Canvas_up(Canvas, Widget_up, UpdateWidget):

    def __init__(self, master=None, cnf={}, **kw) -> None:

        Canvas.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)

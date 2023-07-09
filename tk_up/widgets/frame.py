from tkinter import ttk

from tk_up.widgets.w import Widget_up, UpdateWidget



class Frame_up(ttk.Frame, Widget_up, UpdateWidget):

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

class LabelFrame_up(ttk.Labelframe, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Labelframe.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

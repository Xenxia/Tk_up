from tkinter import ttk, Misc
from typing import Literal, Callable, Any

from tk_up.types import FuncsUpdate

class Widget_up(ttk.Widget):

    #Place
    x: int
    y: int
    width: int
    height: int
    relheight: str|float
    relwidth: str | float
    relx: str | float
    rely: str | float
    place_anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
    bordermode: Literal['inside', 'outside', 'ignore']

    #Grid
    column: int
    columnspan: int
    row: int
    rowspan: int
    grid_ipadx: str | float
    grid_ipady: str | float
    grid_padx: str | float | tuple[str | float, str | float]
    grid_pady: str | float | tuple[str | float, str | float]
    sticky: str

    #Pack
    after: Misc
    pack_anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
    before: Misc
    expand: int
    fill: Literal['none', 'x', 'y', 'both']
    side: Literal['left', 'right', 'top', 'bottom']
    pack_ipadx: str | float
    pack_ipady: str | float
    pack_padx: str | float | tuple[str | float, str | float]
    pack_pady: str | float | tuple[str | float, str | float]

    #Sys
    sysShowHide: str

    def __init__(self):

        self.sysShowHide = "default"

    def placePosSize(self, 
                    x: int = 0, 
                    y: int = 0, 
                    width: int = 0, 
                    height: int = 0, 
                    relheight: str|float = None, 
                    relwidth: str|float = None, 
                    relx: str | float = None, 
                    rely: str | float = None, 
                    anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = None, 
                    bordermode: Literal['inside', 'outside', 'ignore'] = "ignore"
                    ):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.relheight = relheight
        self.relwidth = relwidth
        self.relx = relx
        self.rely = rely
        self.place_anchor = anchor
        self.bordermode = bordermode

        self.sysShowHide = "place"

        return self

    def gridPosSize(self, 
                    row: int = 0, 
                    column: int = 0, 
                    rowspan: int = 1, 
                    columnspan: int = 1, 
                    ipadx: str | float = None, 
                    ipady: str | float = None, 
                    padx: str | float | tuple[str | float, str | float] = None, 
                    pady: str | float | tuple[str | float, str | float] = None, 
                    sticky: str = None
                    ):

        self.row = row
        self.column = column
        self.sticky = sticky
        self.grid_padx = padx
        self.grid_pady = pady
        self.grid_ipadx =ipadx
        self.grid_ipady =ipady
        self.columnspan = columnspan
        self.rowspan = rowspan

        self.sysShowHide = "grid"

        return self

    def packPosSize(self, 
                    after: Misc = None, 
                    anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = None, 
                    before: Misc = None, 
                    expand: int = None, 
                    fill: Literal['none', 'x', 'y', 'both'] = None, 
                    side: Literal['left', 'right', 'top', 'bottom'] = None, 
                    ipadx: str | float = None, 
                    ipady: str | float = None, 
                    padx: str | float | tuple[str | float, str | float] = None, 
                    pady: str | float | tuple[str | float, str | float] = None
                    ):

        self.after = after
        self.pack_anchor = anchor
        self.before = before
        self.expand = expand
        self.fill = fill
        self.side = side
        self.pack_ipadx = ipadx
        self.pack_ipady = ipady
        self.pack_padx = padx
        self.pack_pady = pady

        self.sysShowHide = "pack"

        return self

    def show(self):

        if self.sysShowHide == "place":
            self.place(
                x=self.x, 
                y=self.y, 
                width=self.width, 
                height=self.height, 
                relheight=self.relheight, 
                relwidth=self.relwidth, 
                relx=self.relx, 
                rely=self.rely, 
                anchor=self.place_anchor, 
                bordermode=self.bordermode
                )

        elif self.sysShowHide == "grid":
            self.grid(
                row=self.row, 
                column=self.column, 
                sticky=self.sticky, 
                padx=self.grid_padx, 
                pady=self.grid_pady, 
                ipadx=self.grid_ipadx, 
                ipady=self.grid_ipady, 
                columnspan=self.columnspan, 
                rowspan=self.rowspan
                )

        elif self.sysShowHide == "pack":
            self.pack(
                after=self.after, 
                anchor=self.pack_anchor, 
                before=self.before, 
                expand=self.expand, 
                fill=self.fill, 
                side=self.side, 
                ipadx=self.pack_ipadx, 
                ipady=self.pack_ipady, 
                padx=self.pack_padx, 
                pady=self.pack_pady
                )

        elif self.sysShowHide == "default":
            self.pack()
        else:
            raise ValueError

        return self

    def hide(self):
        if self.sysShowHide == "place":
            self.place_forget()
        elif self.sysShowHide == "grid":
            self.grid_forget()
        elif self.sysShowHide == "pack":
            self.pack_forget()
        elif self.sysShowHide == "default":
            self.pack_forget()
        else:
            raise ValueError

        return self

class UpdateWidget(ttk.Widget):

    def __init__(self, func: FuncsUpdate = []) -> None:
        self.rootWidget: ttk.Widget = self.nametowidget('.')
        self.rootWidget.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.bind("<<TK_UP.Update>>", self.__update, add="+")

        self.updateFunc: FuncsUpdate = func

    def __update(self, event):

        if self.updateFunc.__len__() != 0:
            for f in self.updateFunc:
                f(self, event)

        self.update()

    def addFuncUpdate(self, func: FuncsUpdate):
        self.updateFunc = func

    def updateRoot(self):
        self.rootWidget.update()
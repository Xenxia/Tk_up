from typing import Any

from tk_up.widgets.frame import Frame_up
from tk_up.managerWidgets import ManagerWidgets_up

class TEMPLATE_PAGE(Frame_up):

    # DONT REMOVE THIS
    ctx: dict[str, Any]
    wManager: ManagerWidgets_up

    def __init__(self, context: dict, wManager: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.ctx = context.copy()
        self.wManager = wManager

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.bind("<<TK_UP.Update>>", self.__update, add="+")
        self.nametowidget('.').bind("<<TK_UP.Update>>", self.__update, add="+")

    # this function is call if you hide widget
    def disable(self) -> None:
        pass

    # this function is call if you show widget
    def enable(self) -> None:
        pass
    
    # this function is call if <<TK_UP.Update>> event is call
    def __update(self, event) -> None:
        pass
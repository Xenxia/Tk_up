from typing import Any

from tk_up.widgets.frame import Frame_up
from tk_up.managerWidgets import ManagerWidgets_up

class ManagedFrame(Frame_up):

    ctx: dict[str, Any]
    wManager: ManagerWidgets_up


    # this function is call if you hide widget
    def disable(self) -> None: ...

     # this function is call if you show widget
    def enable(self) -> None: ...

    # this function is call if <<TK_UP.Update>> event is call
    def __update(self, event) -> None: ...
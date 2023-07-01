from tk_up.widgets.frame import Frame_up
from typing import Any

class ManagedFrame(Frame_up):

    ctx: dict[str, Any]

    # this function is call if you hide widget
    def disable(self) -> None: ...

     # this function is call if you show widget
    def enable(self) -> None: ...

    # this function is call if <<TK_UP.Update>> event is call
    def __update(self, event) -> None: ...
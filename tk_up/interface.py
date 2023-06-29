from tk_up.widgets import Frame_up
from typing import Any

class ManagedFrame(Frame_up):

    context: dict[str, Any]

    # this function is call if you hide widget
    def disable(self) -> None:
        pass

     # this function is call if you show widget
    def enable(self) -> None:
        pass
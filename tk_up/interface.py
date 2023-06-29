from tk_up.widgets import Frame_up

class ManagedFrame(Frame_up):

    # this function is call if you hide widget
    def disable(self) -> None:
        pass

     # this function is call if you show widget
    def enable(self) -> None:
        pass
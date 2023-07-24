import importlib, os, pathlib, sys
from genericpath import exists
from typing import Any, Tuple

from tk_up.widgets.frame import Frame_up
from tk_up.interface import ManagedFrame

class ManagerWidgets_up(Frame_up):

    class_widget: dict[str, ManagedFrame] = {}

    def __init__(self, context: dict[str, Any] = {}, asset_folder = "./page", master=None, **kw) -> None:

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])

        if not exists(asset_folder):
            sys.exit(f"folder {asset_folder} not exists")
        
        sys.path.append(asset_folder)

        for ex in ("*.py", "*.pyc"):
            for file in pathlib.Path(asset_folder).glob(ex):
                file_without_extension = os.path.splitext(os.path.basename(file))[0]
                #import page
                import_page = importlib.import_module(str(file_without_extension))
                #load class and give context
                class_p = import_page.__getattribute__(file_without_extension)(context=context, wManager=self, master=self, kw=kw)
                class_p.hide()

                self.class_widget[file_without_extension] = class_p

    def showWidget(self, name_w: str) -> None:

        if name_w in self.class_widget.keys():
            for name, class_ in self.class_widget.items():
                if name != name_w:
                    class_.hide()
                    try:
                        class_.disable()
                    except:
                        pass
                else:
                    class_.show()
                    try:
                        class_.enable()
                    except:
                        pass

    def hideAll(self) -> None:
        for _, class_ in self.class_widget.items():
            class_.hide()
            try:
                class_.disable()
            except:
                pass

    def showAll(self) -> None:
        for _, class_ in self.class_widget.items():
            class_.show()
            try:
                class_.enable()
            except:
                pass

    def getClassWidget(self, name_w: str) -> ManagedFrame:
        return self.class_widget[name_w]

    def getAllClassWidget(self) -> dict[str, ManagedFrame]:
        return self.class_widget

    def addInContextInOneWidget(self, name_w:str, addCtx: Tuple[str, Any] = None) -> bool:

        try:
            ctx: list = self.class_widget[name_w].ctx
        except:
            return False

        if addCtx is not None:
            ctx[addCtx[0]] = addCtx[1]

        return True

    def addInContextInAllWidget(self):
        pass

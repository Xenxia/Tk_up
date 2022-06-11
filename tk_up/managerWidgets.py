import importlib, os, pathlib, sys
from site import execsitecustomize
from genericpath import exists
from typing import Any, Tuple

from tk_up.widgets import Frame_up

class ManagerWidgets_up(Frame_up):

    class_widget: dict = {}

    def __init__(self, parameters_list: list = [], parameters_dict: dict = {}, asset_folder = "./page", master=None, **kw) -> None:

        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])

        if not exists(asset_folder):
            sys.exit(f"folder {asset_folder} not exists")
        
        sys.path.append(asset_folder)

        for ex in ("*.py", "*.pyc"):
            for file in pathlib.Path(asset_folder).glob(ex):
                file_without_extension = os.path.splitext(os.path.basename(file))[0]
                #import page
                import_page = importlib.import_module(str(file_without_extension))
                #load class and give parameter
                class_p = import_page.__getattribute__(file_without_extension)(parameters_list=parameters_list, parameters_dict = parameters_dict, manager_class=self, master=self, kw=kw)
                class_p.hide()

                self.class_widget[file_without_extension] = class_p

    def showWidget(self, name_w: str):

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

    def hideAll(self):
        for _, class_ in self.class_widget.items():
            class_.hide()
            try:
                class_.disable()
            except:
                pass

    def showAll(self):
        for _, class_ in self.class_widget.items():
            class_.show()
            try:
                class_.enable()
            except:
                pass

    def getClassWidget(self, name_w: str) -> Any:
        return self.class_widget[name_w]

    def getAllClassWidget(self) -> dict:
        return self.class_widget

    def addParametersInOneWidget(self, name_w:str, parameter_dict: Tuple[str, Any] = None, parameter_list: Any = None, index: int = None):

        try:
            p_l: list = self.class_widget[name_w].parameters_list
            parLCheck = True
        except:
            parLCheck = False

        try:
            p_d: dict = self.class_widget[name_w].parameters_dict
            parDCheck = True
        except:
            parDCheck = False

        if parameter_list is not None and parLCheck:
            if index == None:
                p_l.append(parameter_list)
            else:
                p_l[index] = parameter_list

        if parameter_dict is not None and parDCheck:
            p_d[parameter_dict[0]] = parameter_dict[1]

    def addParametersInAllWidget(self):
        pass

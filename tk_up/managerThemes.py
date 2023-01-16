
from genericpath import exists
import os, pathlib, sys, tkinter
from tkinter import Tk, ttk

from widgets import Tk_up


class ManagerThemes():

    master: Tk
    list_themes: list = []
    themes: dict = {}
    use_theme: str
    style: ttk.Style

    def __init__(self, master: Tk_up, themes_folder="themes") -> None:
        self.master = master
        self.style = ttk.Style()

        if not exists(themes_folder):
            sys.exit(f"folder {themes_folder} not exists")

        for theme in pathlib.Path(themes_folder).glob("*.thm"):
            theme_name = os.path.splitext(os.path.basename(theme))[0]
            theme_tcl = f"main.tcl"
            theme_path = os.path.join(theme, theme_tcl)

            self.list_themes.append(theme_name)
            self.themes[theme_name] = theme_path

    def setTheme(self, name: str, themes: str = "light"):

        if name in self.list_themes:
            self.master.tk.call("source", f"{self.themes[name]}")
            self.master.tk.call("set_theme", f"{themes}")
            self.use_theme = name
        else:
            raise KeyError(f"'{name}' is not valide theme")

        return self

    def switch_Light_Dark_Theme(self):
        if self.master.tk.call("ttk::style", "theme", "use") == f"{self.use_theme}-dark":
            # Set light theme
            self.master.tk.call("set_theme", "light")
        else:
            # Set dark theme
            self.master.tk.call("set_theme", "dark")

        return self

    def get_info_element(self, element):
        try:
            # Get widget elements
            style = ttk.Style()
            layout = str(style.layout(element))
            print('Stylename = {}'.format(element))
            print('Layout    = {}'.format(layout))
            elements=[]
            for n, x in enumerate(layout):
                if x=='(':
                    element=""
                    for y in layout[n+2:]:
                        if y != ',':
                            element=element+str(y)
                        else:
                            elements.append(element[:-1])
                            break
            print('Element(s) = {}\n'.format(elements))

            # Get options of widget elements
            for element in elements:
                print('{0:30} options: {1}'.format(
                    element, style.element_options(element)))
            print("\n")

        except tkinter.TclError:
            print('_tkinter.TclError: "{0}" in function'
                'widget_elements_options({0}) is not a regonised stylename.'
                .format(element))

    def get_theme_use(self) -> str:
        return self.style.theme_use()

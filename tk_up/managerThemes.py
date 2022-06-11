
from genericpath import exists
import os, pathlib, sys
from tkinter import Tk

class ManagerThemes():

    master: Tk
    list_themes: list = []
    themes: dict = {}
    use_theme: str

    def __init__(self, master, themes_folder="themes") -> None:
        self.master = master

        if not exists(themes_folder):
            sys.exit(f"folder {themes_folder} not exists")

        for theme in pathlib.Path(themes_folder).glob("*.thm"):
            theme_name = os.path.splitext(os.path.basename(theme))[0]
            theme_tcl = f"{theme_name}.tcl"
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

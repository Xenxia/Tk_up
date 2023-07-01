import re as regex
from tkinter import ttk, Tk
from typing import Any
from tkinter.constants import BOTH, LEFT, RIGHT, X

from tk_up.widgets import PLATFORM_SYS
from tk_up.widgets.button import Button_up
from tk_up.widgets.label import Label_up

if PLATFORM_SYS == "Windows":
    from ctypes import windll

def setAppWindow(mainWindow, windows = None): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True)
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic

    hwnd: Any

    if windows is None:
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    else:
        hwnd = windll.user32.GetParent(windows.winfo_id())

    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    if windows is None:
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    else:
        windows.wm_withdraw()
        windows.wm_deiconify()


class Tk_up(Tk, ttk.Frame):

    titleBarComponent: list
    funcRunAfter: list = []
    customTitleBar: bool
    root: Tk

    # Title bar info
    activeComp: dict = {
        'titleBarTitle': True,
        'closeButton': True,
        'expandButton': True,
        'minimizeButton': True,
    }
    title: str
    geometry: str

    # Size screen
    rootHeigth: int
    rootWidth: int

    # Component
    __titleBar: ttk.Frame

    def __init__(self, customTitleBar:bool=False) -> None:
        self.customTitleBar=customTitleBar

        if customTitleBar:
            self.root = Tk()
            self.root.event_add("<<TK_UP.Update>>", "None")
            self.rootHeigth = self.root.winfo_screenheight()
            self.rootWidth = self.root.winfo_screenwidth()
            self.root.minimized = False
            self.root.maximized = False
            self.root.overrideredirect(True)
            self.__titleBar = ttk.Frame(self.root, relief='raised', bd=0, highlightthickness=0)
            self.titleBarTitle = Label_up(self.__titleBar, bd=0, fg='white', font=("helvetica", 10), highlightthickness=0)
            self.closeButton = Button_up(self.__titleBar, text=' 🗙 ', command=self.root.destroy, font=("calibri", 11), bd=0, fg='white', highlightthickness=0)
            self.expandButton = Button_up(self.__titleBar, text=' 🗖 ', bd=0, fg='white', font=("calibri", 11), highlightthickness=0)
            self.minimizeButton = Button_up(self.__titleBar, text=' 🗕 ', bd=0, fg='white', font=("calibri", 11), highlightthickness=0)
            self.titleBarComponent = [
                self.__titleBar,
                self.titleBarTitle,
                self.minimizeButton,
                self.closeButton,
                self.expandButton
            ]
            if PLATFORM_SYS == "Windows":
                self.runAfterMainloopStarted(lambda: setAppWindow(self.root))
            ttk.Frame.__init__(self, master=self.root ,highlightthickness=0)
        else:
            Tk.__init__(self)
            self.rootWidth = self.winfo_screenwidth()
            self.rootHeigth = self.winfo_screenheight()


        self.event_add("<<TK_UP.Update>>", "None")
        

    def __getPos(self, event):

        if self.root.maximized == False:
            
            xwin = self.root.winfo_x()
            ywin = self.root.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event): # runs when window is dragged
                self.root.config(cursor="fleur")
                self.root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


            def release_window(event): # runs when window is released
                self.root.config(cursor="arrow")
                
            self.__titleBar.bind('<B1-Motion>', move_window)
            self.__titleBar.bind('<ButtonRelease-1>', release_window)
            # title_bar_title.bind('<B1-Motion>', move_window)
            # title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            self.expandButton.config(text=" 🗖 ")
            self.root.maximized = not self.root.maximized

    def configWindows(self, title:str="Tk_Up", geometry:str="500x500", iconbitmap:str=None):

        if regex.findall(r"\+center", geometry) != []:
            gSizeW, gSizeH = geometry.split("+", 1)[0].split("x", 1)
            rootH = round((self.rootHeigth/2)-(int(gSizeH)/2))
            rootW = round((self.rootWidth/2)-(int(gSizeW)/2))
            geometry = f'{gSizeW}x{gSizeH}+{rootW}+{rootH}'
        
        if self.customTitleBar:
            self.titleBarTitle.configure(text=title)
        
            self.root.title(title)
            self.root.geometry(geometry)

            if iconbitmap is not None:
                self.root.iconbitmap(iconbitmap)

        else:
            self.title(title)
            self.geometry(geometry)
            if iconbitmap is not None:
                self.iconbitmap(iconbitmap)

    def configTitleBar(self, color:str="#ffffff", active:dict[str, bool]=None, c_closeButton:dict=None):

        if self.customTitleBar:

            if active is not None:
                self.activeComp.update(active)

            for comp in self.titleBarComponent:
                comp.configure(bg=color)

    def runAfterMainloopStarted(self, func: Any):
        self.funcRunAfter.append(func)

    def run(self):
        if self.customTitleBar:
            self.__titleBar.bind('<Button-1>', self.__getPos)
            self.__titleBar.pack(side="top", fill=X)
            if self.activeComp['titleBarTitle']: self.titleBarTitle.pack(side=LEFT, padx=(10, 0))
            if self.activeComp['closeButton']: self.closeButton.pack(side=RIGHT)
            if self.activeComp['expandButton']: self.expandButton.pack(side=RIGHT)
            if self.activeComp['minimizeButton']: self.minimizeButton.pack(side=RIGHT)
            self.pack(expand=1, fill=BOTH)
            for func in self.funcRunAfter:
                self.root.after(10, func)
            self.root.mainloop()
        else:
            if self.funcRunAfter == []:
                for func in self.funcRunAfter:
                    self.after(10, func)
            self.mainloop()

    def updateEvent(self) -> None:
        if self.customTitleBar:
            self.root.event_generate("<<TK_UP.Update>>")
        else:
            self.event_generate("<<TK_UP.Update>>")

import platform, re as regex
from tkinter import Canvas, Grid, IntVar, Misc, Pack, Place, StringVar, Text, Tk, Toplevel, ttk
import tkinter
from typing import Any, Literal, Tuple
from tkinter.constants import BOTH, BOTTOM, DISABLED, END, HORIZONTAL, LEFT, NO, NORMAL, RIGHT, VERTICAL, W, X, Y, YES
from PIL import Image, ImageTk, ImageColor
from copy import copy

PLATFORM_SYS = platform.system()

if PLATFORM_SYS == "Windows":
    from ctypes import windll

SCROLL_X: str = "scroll_x"
SCROLL_Y: str = "scroll_y"
SCROLL_ALL: str = "scroll_all"

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

#CLASS sys

class ScrolledText(Text):

    def __init__(self, master=None, **kw):

        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)

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

class Widget_up(ttk.Widget):

    #Place
    x: int
    y: int
    width: int
    height: int
    relheight: str|float
    relwidth: str | float
    relx: str | float
    rely: str | float
    place_anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
    bordermode: Literal['inside', 'outside', 'ignore']

    #Grid
    column: int
    columnspan: int
    row: int
    rowspan: int
    grid_ipadx: str | float
    grid_ipady: str | float
    grid_padx: str | float | tuple[str | float, str | float]
    grid_pady: str | float | tuple[str | float, str | float]
    sticky: str

    #Pack
    after: Misc
    pack_anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
    before: Misc
    expand: int
    fill: Literal['none', 'x', 'y', 'both']
    side: Literal['left', 'right', 'top', 'bottom']
    pack_ipadx: str | float
    pack_ipady: str | float
    pack_padx: str | float | tuple[str | float, str | float]
    pack_pady: str | float | tuple[str | float, str | float]

    #Sys
    sysShowHide: str

    def __init__(self):

        self.sysShowHide = "default"

    def placePosSize(self, 
                    x: int = 0, 
                    y: int = 0, 
                    width: int = 0, 
                    height: int = 0, 
                    relheight: str|float = None, 
                    relwidth: str|float = None, 
                    relx: str | float = None, 
                    rely: str | float = None, 
                    anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = None, 
                    bordermode: Literal['inside', 'outside', 'ignore'] = "ignore"
                    ):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.relheight = relheight
        self.relwidth = relwidth
        self.relx = relx
        self.rely = rely
        self.place_anchor = anchor
        self.bordermode = bordermode

        self.sysShowHide = "place"

        return self

    def gridPosSize(self, 
                    row: int = 0, 
                    column: int = 0, 
                    rowspan: int = 1, 
                    columnspan: int = 1, 
                    ipadx: str | float = None, 
                    ipady: str | float = None, 
                    padx: str | float | tuple[str | float, str | float] = None, 
                    pady: str | float | tuple[str | float, str | float] = None, 
                    sticky: str = None
                    ):

        self.row = row
        self.column = column
        self.sticky = sticky
        self.grid_padx = padx
        self.grid_pady = pady
        self.grid_ipadx =ipadx
        self.grid_ipady =ipady
        self.columnspan = columnspan
        self.rowspan = rowspan

        self.sysShowHide = "grid"

        return self

    def packPosSize(self, 
                    after: Misc = None, 
                    anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = None, 
                    before: Misc = None, 
                    expand: int = None, 
                    fill: Literal['none', 'x', 'y', 'both'] = None, 
                    side: Literal['left', 'right', 'top', 'bottom'] = None, 
                    ipadx: str | float = None, 
                    ipady: str | float = None, 
                    padx: str | float | tuple[str | float, str | float] = None, 
                    pady: str | float | tuple[str | float, str | float] = None
                    ):

        self.after = after
        self.pack_anchor = anchor
        self.before = before
        self.expand = expand
        self.fill = fill
        self.side = side
        self.pack_ipadx = ipadx
        self.pack_ipady = ipady
        self.pack_padx = padx
        self.pack_pady = pady

        self.sysShowHide = "pack"

        return self

    def show(self):

        if self.sysShowHide == "place":
            self.place(
                x=self.x, 
                y=self.y, 
                width=self.width, 
                height=self.height, 
                relheight=self.relheight, 
                relwidth=self.relwidth, 
                relx=self.relx, 
                rely=self.rely, 
                anchor=self.place_anchor, 
                bordermode=self.bordermode
                )

        elif self.sysShowHide == "grid":
            self.grid(
                row=self.row, 
                column=self.column, 
                sticky=self.sticky, 
                padx=self.grid_padx, 
                pady=self.grid_pady, 
                ipadx=self.grid_ipadx, 
                ipady=self.grid_ipady, 
                columnspan=self.columnspan, 
                rowspan=self.rowspan
                )

        elif self.sysShowHide == "pack":
            self.pack(
                after=self.after, 
                anchor=self.pack_anchor, 
                before=self.before, 
                expand=self.expand, 
                fill=self.fill, 
                side=self.side, 
                ipadx=self.pack_ipadx, 
                ipady=self.pack_ipady, 
                padx=self.pack_padx, 
                pady=self.pack_pady
                )

        elif self.sysShowHide == "default":
            self.pack()
        else:
            raise ValueError

        return self

    def hide(self):
        if self.sysShowHide == "place":
            self.place_forget()
        elif self.sysShowHide == "grid":
            self.grid_forget()
        elif self.sysShowHide == "pack":
            self.pack_forget()
        elif self.sysShowHide == "default":
            self.pack_forget()
        else:
            raise ValueError

        return self

# Widget up

class Toplevel_up(Toplevel, ttk.Frame):

    top: Toplevel
    # Size screen
    rootHeigth: int
    rootWidth: int

    def __init__(self, master=None, cnf={}, **kw):

        Toplevel.__init__(self, master=master, cnf=cnf, **kw)
        self.rootWidth = self.winfo_screenwidth()
        self.rootHeigth = self.winfo_screenheight()
        self.protocol("WM_DELETE_WINDOW", self.hide)

    def configWindows(self, title:str="Tk_Up", geometry:str="500x500", iconbitmap:str=None):

        if regex.findall(r"\+center", geometry) != []:
            gSizeW, gSizeH = geometry.split("+", 1)[0].split("x", 1)
            rootH = round((self.rootHeigth/2)-(int(gSizeH)/2))
            rootW = round((self.rootWidth/2)-(int(gSizeW)/2))
            geometry = f'{gSizeW}x{gSizeH}+{rootW}+{rootH}'

        self.title(title)
        self.geometry(geometry)
        if iconbitmap is not None:
            self.iconbitmap(iconbitmap)

        return self

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

class Button_up(ttk.Button, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Button.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

    def disable(self):
        self['state'] = DISABLED

    def enable(self):
        self['state'] = NORMAL

class Toggle_Button_up(Button_up):

    text: Tuple = ("ON", "OFF")
    style: Tuple = None
    status: bool

    def __init__(self, master=None, **kw):
        Button_up.__init__(self, master=master, **kw, command=self.toggle)
        self.status = True
        self.reload()
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def reload(self):
        if self.status:
            self.config(text=self.text[0])
            if self.style is not None: self.config(style=self.style[0])
            self.status = True
        else:
            self.config(text=self.text[1])
            if self.style is not None: self.config(style=self.style[1])
            self.status = False

    def custom_toggle(self, text: Tuple = None, style: Tuple = None):
        if text is not None: self.text = text
        if style is not None: self.style = style
        self.reload()

    def set_default_status(self, status: bool):
        self.status = status
        self.reload()

    def get_status(self) -> bool:
        return self.status

    def toggle(self):
    
        if self.config('text')[-1] == self.text[0]:
            self.config(text=self.text[1])
            if self.style is not None: self.config(style=self.style[1])
            self.status = False
        else:
            self.config(text=self.text[0])
            if self.style is not None: self.config(style=self.style[0])
            self.status = True

class Checkbutton_up(ttk.Checkbutton, Widget_up):

    variable: StringVar

    def __init__(self, master=None, **kw):
        self.variable = StringVar()

        ttk.Checkbutton.__init__(self, master=master, variable=self.variable, onvalue=1, offvalue=0, **kw)
        Widget_up.__init__(self)

    def disable(self):
        self['state'] = DISABLED

    def enable(self):
        self['state'] = NORMAL

    def get(self):
        return self.variable

class Label_up(ttk.Label, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Label.__init__(self, master=master, **kw)
        Widget_up.__init__(self)



class Text_up(Text, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        Text.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class ScrolledText_up(ScrolledText, Widget_up):

    def __init__(self, master=None, cnf={}, **kw) -> None:
        ScrolledText.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class Terminal_ScrolledText_up(ScrolledText, Widget_up):

    def __init__(self, master=None, cnf={}, **kw):
        ScrolledText.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)
        self.bind("<Key>", lambda e: self.__ctrlEvent(e))

    def __ctrlEvent(self, event) -> None:
        if(12==event.state and event.keysym=='c' ):
            return
        else:
            return "break"

    def configTag(self, tag: dict):
        for key, value in tag.items():
            self.tag_configure(key, background=value[0], foreground=value[1])

    def printTerminal(self, *texts, color: list = None) -> None:
        for index, text in enumerate(texts):
            if text == texts[-1]:
                self.insert(END, text+ "\n", color[index])
            else:
                self.insert(END, text, color[index])
        self.see(END)

    def clearTerminal(self) -> None:
        self.delete("1.0","end")

class Canvas_up(Canvas, Widget_up):

    def __init__(self, master=None, cnf={}, **kw) -> None:

        Canvas.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)

class Treeview_up(ttk.Frame, Widget_up):
    __count: int = 10
    __iid: bool
    __child: bool
    tree: ttk.Treeview
    scroll_y: ttk.Scrollbar
    scroll_x: ttk.Scrollbar

    def __init__(self, master=None, scroll:str=None, iid:bool=False, child:bool=False, show="tree", selectmode="browse", indent=10, **kw):

        ttk.Frame.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

        self.propagate(False)

        self.__child=child
        self.__iid=iid

        self.tree = ttk.Treeview(
            master=self,
            show=show,
            selectmode=selectmode,
            height=(kw["height"] if "height" in kw else None),
        )

        if scroll != None:
            self.scroll_y = ttk.Scrollbar(master=self, orient=VERTICAL)
            self.scroll_y.pack(side=RIGHT, fill=Y)

            self.scroll_x = ttk.Scrollbar(master=self, orient=HORIZONTAL)
            self.scroll_x.pack(side=BOTTOM, fill=X)

            if scroll == SCROLL_X:
                self.scroll_x.config(command=self.tree.xview)
                self.tree.configure(xscrollcommand=self.scroll_x.set)
                self.scroll_y.destroy()

            if scroll == SCROLL_Y:
                self.scroll_y.config(command=self.tree.yview)
                self.tree.configure(yscrollcommand=self.scroll_y.set)
                self.scroll_x.destroy()

            if scroll == SCROLL_ALL:
                self.scroll_x.config(command=self.tree.xview)
                self.scroll_y.config(command=self.tree.yview)

                self.tree.configure(xscrollcommand=self.scroll_x.set)
                self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.tree.pack(fill="x", expand=True)

        self.tree['columns'] = ("empty")

    def __popItem(self, dict:dict, position=0):

        key = list(dict.keys())[position]
        value = list(dict.values())[position]

        del dict[key]

        return (key, value), dict

    def __getSubChildren(self, tree, item=""):
        children: list = []
        list_children = tree.get_children(item)
        for child in list_children:
            children.append(child)
            children += self.__getSubChildren(tree, child)
        return children

    def bind(self, sequence:str|None= None, func=None, add:bool|Literal['', '+']|None=None) -> None:
        self.tree.bind(sequence=sequence, func=func, add=add)

    def setTag(self, nameTag:str, bg:str=None, fg:str=None, image:str=None, font:str=None):
        self.setTags(({
            "name": nameTag,
            "bg": bg,
            "fg": fg,
            "image": image,
            "font": font,
            }))

    def setTags(self, tags: Tuple[dict]):

        for tag in tags:

            try:
                name = tag["name"]
            except:
                return

            try:
                bg = tag["bg"]
                self.tree.tag_configure(tagname=name, background=bg)
            except:
                pass
            
            try:
                fg = tag["fg"]
                self.tree.tag_configure(tagname=name, foreground=fg)
            except:
                pass

            try:
                image = tag["image"]
                self.tree.tag_configure(tagname=name, image=image)
            except:
                pass

            try:
                font = tag["font"]
                self.tree.tag_configure(tagname=name, font=font)
            except:
                pass

    def addElements(self, data:dict=None) -> bool:

        temp: dict = {}

        while True:
            
            if len(data) == 0:
                data = temp
                temp = {}
            
            if (len(data) + len(temp)) == 0:
                return True

            while len(data) != 0:
                
                child, data = self.__popItem(data)

                print(child)

                if child[1]["parent"] not in data:
                    
                    iid: str = child[0]
                    parent: str = str(child[1]["parent"]) if child[1]["parent"] is not None else ""
                    
                    # Try Key values
                    try:
                        values: list | Tuple = child[1]["values"]
                    except KeyError:
                        print("values key")
                    # Try Key text
                    try:
                        text: str = child[1]["text"]
                    except KeyError:
                        text = ""

                    # Try Key image
                    try: 
                        image: Any = child[1]["image"] 
                    except KeyError: 
                        image = ""

                    # Try Key open
                    try:
                        open: bool = child[1]["open"]
                    except KeyError:
                        open = False

                    # Try Key tags
                    try:
                        tags: str = child[1]["tags"]
                    except KeyError:
                        tags = ""

                    if self.__child:
                        text = values.pop(0)

                    try:
                        self.tree.insert(
                                parent=parent, 
                                index=END,
                                iid=iid,
                                text=text, 
                                values=values, 
                                tags=tags, 
                                image=image, 
                                open=open
                            )
                    except tkinter.TclError:
                        return False

                    self.__count += 1
                else:
                    temp[child[0]] = child[1]

    def addElement(self, parent:str="", index:int|Literal['end']=END, iid:str=None, id:str="", text:str="", image="", values:list=[], open:bool=False, tags:str|list[str]|Tuple[str, ...]="") -> bool:
        if iid is None:
            iid = self.__count

        if self.__iid and iid is None:
            iid=values[0]

        if self.__child:
            text=values.pop(0)

        try:
            self.tree.insert(parent=parent, index=index, iid=iid, text=text, image=image, values=values, open=open, tags=tags)
            self.__count += 1
        except tkinter.TclError as error:
            return error
        return True

    # def removeOneElement(self):
    #     item = self.tree.selection()[0]
    #     self.tree.delete(item)

    def removeAllElement(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    def removeSelectedElement(self):
        item = self.tree.selection()[0]
        self.tree.delete(item)

    def editSelectedElement(self, text:str="", image="", values:list|Literal['']="", open:bool=False, tags:str|list[str]|tuple[str, ...]=""):
        item = self.tree.focus()
        self.tree.item(item, text=text, image=image, values=values, open=open, tags=tags)

    def editElement(self, item:str, text:str="", image="", values:list|Literal['']="", open:bool=False, tags:str|list[str]|tuple[str, ...]="") -> None:
        self.tree.item(item, text=text, image=image, values=values, open=open, tags=tags)

    def getItemSelectedElemnt(self, option:str='values') -> Any:
        item = self.tree.focus()

        if self.__child and option == "values":
            listValues: list = []
            listValues.append(self.tree.item(item, "text"))
            for value in self.tree.item(item, "values"):
                listValues.append(value)
            return listValues

        return self.tree.item(item, option)

    def getSelectedElement(self) -> tuple:
        return self.tree.selection()

    def getAllChildren(self) -> dict:
        childs_list = self.__getSubChildren(self.tree)

        children_dict = {}

        for iid in childs_list:

            temp_dict = {}

            item = self.tree.item(iid)

            temp_dict["values"] = item["values"]
            temp_dict["text"] = item["text"]
            temp_dict["image"] = item["image"]
            temp_dict["open"] = item["open"]
            temp_dict["tags"] = item["tags"]
            temp_dict["parent"] = None

            parentIID = self.tree.parent(iid)

            if parentIID != "":
                temp_dict["parent"] = parentIID
            
            children_dict[iid] = (temp_dict)
        
        return children_dict

    def getAllParentItem(self, iidParent: str) -> list[str]:

        parentList = []

        while iidParent != '':
            parentList.append(iidParent)
            iidParent = self.tree.parent(iidParent)
        return parentList

    def getItem(self, iid: str) -> tuple | str:
        return self.tree.item(iid)

    def setColumns(self, columns: list[str], anchor: list[str] = None, stretch: list[bool] = None, minSize: list[int] = None, size: list[int] = None) -> None:

        if self.__child:

            if size is not None and len(columns) == len(size):
                self.tree.column("#0", width=size.pop(0))

            if minSize is not None and len(columns) == len(minSize):
                self.tree.column("#0", minwidth=minSize.pop(0))

            if anchor is not None and len(columns) == len(anchor):
                self.tree.column("#0", anchor=anchor.pop(0))

            if stretch is not None and len(columns) == len(stretch):
                self.tree.column("#0", stretch=stretch.pop(0))
            else:
                self.tree.column("#0", stretch=NO)

            firstColumn = columns.pop(0)

            self.tree['columns'] = columns
            self.tree.heading("#0", text=firstColumn)
        else:
            self.tree['columns'] = columns
            self.tree.column("#0", width=0, stretch=NO)
            self.tree.heading("#0", text="")

        end = columns[-1]

        for index, col in enumerate(columns):

            if size is not None and len(columns) == len(size):
                self.tree.column(col, width=size[index])
            else:
                self.tree.column(col, width=100)

            if minSize is not None and len(columns) == len(minSize):
                self.tree.column(col, minwidth=minSize[index])

            if anchor is not None and len(columns) == len(anchor):
                self.tree.column(col, anchor=anchor[index])
            # else:
            #     self.tree.column(col, anchor="center")

            if stretch is not None and len(columns) == len(stretch):
                self.tree.column(col, stretch=stretch[index])

            if end == col and stretch is None:
                self.tree.column(col, stretch=YES)
            elif stretch is None:
                self.tree.column(col, stretch=NO)

            self.tree.heading(col, text=col)

    def moveUpSelectedElement(self) -> None:
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)-1)

    def moveDownSelectedElement(self) -> None:
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)+1)

class Frame_up(ttk.Frame, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

class Frame_alphaBg_up(Canvas_up):

    # color 
    alpha: int
    color: Tuple[int]

    def __init__(self, master=None, width=200, height=200, cnf={}, **kw) -> None:

        if "alpha" in kw: 
            self.alpha = int(kw.pop('alpha')*255)
        else: 
            self.alpha = 255

        if "color" in kw: 
            self.color = ImageColor.getcolor(kw.pop('color'), "RGB")
        else:
            self.color = (255, 255, 255)

        self.img = []

        i=Image.new('RGBA', (width, height), self.color + (self.alpha,))

        self.img.append(ImageTk.PhotoImage(i))

        Canvas.__init__(self, master=master, width=width, height=height, cnf=cnf, **kw)
        self.config(highlightthickness=0)
        self.create_image(0, 0, image=self.img[-1])


    def addWidget(self, widget, x, y):
        self.create_window(x, y, widget)
        return self

class LabelFrame_up(ttk.Labelframe, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Labelframe.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

class Entry_up(ttk.Entry, Widget_up):

    def __init__(self, master=None, **kw):
        ttk.Entry.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

class OptionMenu_up(ttk.Combobox, Widget_up):

    def __init__(self, master=None, style=None, type: str="str", default: int=None, list: Tuple | list=None, **kw) -> None:

        type_var: StringVar | IntVar

        if type == "str":
            type_var = StringVar()
        elif type == "int":
            type_var = IntVar()

        ttk.Combobox.__init__(self, master, values=list ,textvariable=type_var, state="readonly", **kw)
        Widget_up.__init__(self)

class Separator_up(ttk.Separator, Widget_up):

    def __init__(self, master=None, cursor=None, name:str=None, orient:Literal["horizontal", "vertical"]="horizontal", style:str=None, takefocus=None) -> None:

        ttk.Separator.__init__(self, master=master, cursor=cursor, name=name, orient=orient, style=style, takefocus=takefocus)
        Widget_up.__init__(self)

class Tab_up(ttk.Notebook, Widget_up):

    tabs: dict[str, tuple[int, Frame_up]] = {}
    __num: int = 0

    def __init__(self, master=None, cursor=None) -> None:
        ttk.Notebook.__init__(self, master=master, cursor=cursor)
        Widget_up.__init__(self)

    def add_tab(self, name: str) -> Frame_up:

        frame = Frame_up(self)

        self.tabs[name] = copy((self.__num, copy(frame)))

        self.add(self.tabs[name][1], text=name)

        self.__num += 1

        return self.tabs[name][1]

    def get_tab(self, name: str) -> Frame_up:
        return self.tabs[name][1]

    def disable_tab(self, name: str):
        self.tab(self.tabs[name][0], state="disabled")

    def enable_tab(self, name: str):
        self.tab(self.tabs[name][0], state="normal")

    def del_tab(self, name: str):
        self.forget(self.tabs[name][0])
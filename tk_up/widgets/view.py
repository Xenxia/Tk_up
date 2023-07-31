from time import sleep
import tkinter
from typing import Any, Literal, Tuple
from tkinter import ttk
from tkinter.constants import BOTTOM, END, HORIZONTAL, NO, RIGHT, VERTICAL, X, Y, YES

from tk_up.widgets.entry import Entry_up
from tk_up.widgets.w import Widget_up, UpdateWidget

from tk_up.enum import Scroll

from tk_up.types.view import ItemDict, PItemDict, Tag

class _BaseTreeView(ttk.Frame, Widget_up, UpdateWidget):
    _count: int = 0
    _child: bool
    _editRow: bool
    _resizeCol: bool
    _column: list[str, int]
    tree: ttk.Treeview
    scroll_y: ttk.Scrollbar
    scroll_x: ttk.Scrollbar

    def __init__(self, master=None, scroll:Scroll=None, child:bool=False, selectmode: Literal['extended', 'browse', 'none']="browse", indent: int=10, resizeColumn: bool=True, editRow: bool=False, **kw) -> "_BaseTreeView":

        ttk.Frame.__init__(self, master=master, **kw)
        Widget_up.__init__(self)

        self.propagate(False)

        self._child=child
        self._editRow=editRow
        self._resizeCol = resizeColumn

        self.tree = ttk.Treeview(
            master=self,
            selectmode=selectmode,
            height=(kw["height"] if "height" in kw else None),
        )

        UpdateWidget.__init__(self)

        if scroll != None:
            self.scroll_y = ttk.Scrollbar(master=self, orient=VERTICAL)
            self.scroll_y.pack(side=RIGHT, fill=Y)

            self.scroll_x = ttk.Scrollbar(master=self, orient=HORIZONTAL)
            self.scroll_x.pack(side=BOTTOM, fill=X)

            if scroll == Scroll.X:
                self.scroll_x.config(command=self.tree.xview)
                self.tree.configure(xscrollcommand=self.scroll_x.set)
                self.scroll_y.destroy()

            if scroll == Scroll.Y:
                self.scroll_y.config(command=self.tree.yview)
                self.tree.configure(yscrollcommand=self.scroll_y.set)
                self.scroll_x.destroy()

            if scroll == Scroll.ALL:
                self.scroll_x.config(command=self.tree.xview)
                self.scroll_y.config(command=self.tree.yview)

                self.tree.configure(xscrollcommand=self.scroll_x.set)
                self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.tree.pack(fill="x", expand=True)

        self.tree['columns'] = ("empty")

        
        self.tree.bind('<Button-1>', self.__prevent_resize, add="+")
        self.tree.bind('<Button-1>', self.__updateRowColSelect, add="+")
        self.tree.bind('<Double-Button-1>', self.__onDoubleclick, add="+")
        self.tree.bind('<Double-1>', lambda e: 'break', add="+")
        # self.tree.bind('<Motion>', self.__prevent_resize)

    def __popItem(self, dict:dict, position=0) -> tuple[tuple[str, Any], dict]:

        key = list(dict.keys())[position]
        value = list(dict.values())[position]

        del dict[key]

        return (key, value), dict

    def __getSubChildren(self, iid="") -> list | Any:
        children: list = []
        childs = self.tree.get_children(iid)
        for child in childs:
            children.append(child)
            children += self.__getSubChildren(child)
        return children

    def __prevent_resize(self, event) -> Literal["break"] | None:
        if self.tree.identify_region(event.x, event.y) == "separator" and not self._resizeCol:
            return "break"
        
    def __updateRowColSelect(self, event) -> None:
            t = self.tree.identify_column(event.x)
            self._column = [t, int(t.replace("#", ""))]

    def __onDoubleclick(self, event) -> None:

        if self._editRow:
            self.__editPopup(event)

    def __editPopup(self, event) -> None:
        rowid = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        try:
            # get column position info
            x,y,width,height = self.tree.bbox(rowid, column)

            # y-axis offset
            # pady = height // 2
            pady = 0

            # place Entry popup properly
            text = self.getValueSelectedColRow()
            self.entryPopup = _EntryPopup(self, rowid, text, self._column[1])
            self.entryPopup.place(x=x, y=y+pady, width=width, height=height)
        except ValueError as e:
            print(e)

    def bind(self, sequence:str|None= None, func=None, add:bool|Literal['', '+']|None=None) -> None:
        self.tree.bind(sequence=sequence, func=func, add=add)


#======== Setter
    def setTag(self, nameTag:str, bg:str=None, fg:str=None, image:str=None, font:str=None) -> None:
        self.setTags(({
                "name": nameTag,
                "bg": bg,
                "fg": fg,
                "image": image,
                "font": font,
            }))

    def setTags(self, tags: Tuple[Tag]) -> None:

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

#======== Add
    def addItems(self, Items:dict[str, PItemDict]=None) -> bool:

        temp: PItemDict = {}

        while True:
            
            if len(Items) == 0:
                Items = temp
                temp = {}
            
            if (len(Items) + len(temp)) == 0:
                return True

            while len(Items) != 0:
                
                item: tuple[str, PItemDict]; Items: PItemDict
                item, Items = self.__popItem(Items)

                if item[1]["parent"] not in Items:
                    
                    iid: str = item[0]
                    parent: str = str(item[1]["parent"]) if item[1]["parent"] is not None else ""
                    
                    # Try Key values
                    try:
                        values: list | Tuple = item[1]["values"]
                    except KeyError:
                        print("values key")
                    # Try Key text
                    try:
                        text: str = item[1]["text"]
                    except KeyError:
                        text = ""

                    # Try Key image
                    try: 
                        image: Any = item[1]["image"] 
                    except KeyError: 
                        image = ""

                    # Try Key open
                    try:
                        open: bool = item[1]["open"]
                    except KeyError:
                        open = False

                    # Try Key tags
                    try:
                        tags: str = item[1]["tags"]
                    except KeyError:
                        tags = ""

                    if self._child:
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

                    self._count += 1
                else:
                    temp[item[0]] = item[1]

    def addItem(self, parent:str="", index:int|Literal['end']=END, iid:str=None, image="", values:list=[], open:bool=False, tags:str|list[str]|Tuple[str, ...]="") -> tuple[bool, str] | tkinter.TclError:
        if iid is None:
            iid = self._count

        if self._child:
            text=values.pop(0)
        else:
            text=""

        try:
            self.tree.insert(parent=parent, index=index, iid=iid, text=text, image=image, values=values, open=open, tags=tags)
            self._count += 1
        except tkinter.TclError as error:
            return (False, "")

        return (True, iid)

    def addEmptyRow(self) -> None:
        iid = self.addItem()[1]

        self.tree.yview_scroll(self._count, "units")
        self.tree.see(iid)


        col = ("#0", 0) if self._child else ("#1", 1)

        x,y,width,height = self.tree.bbox(iid, col[0])

        
        # y-axis offset
        # pady = height // 2
        pady = 0

        # place Entry popup properly
        # text = self.getValueSelectedColRow()
        self.entryPopup = _EntryPopup(self, iid, "", col[1])
        self.entryPopup.place(x=x, y=y+pady, width=width, height=height)


#======== Remove
    def removeAllItems(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    def removeSelectedItem(self):
        items = self.tree.selection()
        for item in items:
            self.tree.delete(item)

    def removeItem(self, iid: str):
        self.tree.delete(iid)

#======== Edit
    def editSelectedItem(self, image=None, values:list|Literal['']=None, open:bool=False, tags:str|list[str]|tuple[str, ...]=None) -> None:
        item = self.tree.focus()
        
        self.editItem(item, image, values, open, tags)

    def editItem(self, iid:str, image=None, values:list|Literal['']=None, open:bool=False, tags:str|list[str]|tuple[str, ...]=None) -> None:
        if self._child and values is not None:
            self.tree.item(iid, text=values.pop(0))
        
        if image != None:
            self.tree.item(iid, image=image)

        if values != None:
            self.tree.item(iid, values=values)

        if open:
            self.tree.item(iid, open=open)

        if tags != None:
            self.tree.item(iid, tags=tags)

        if self.isEmptyRow(iid):
            self.removeItem(iid)

    def editValueColRow(self, value: Any, column: int, rowId: str) -> None:

            t: list = self.getItem(rowId)["values"]

            if len(t) == 0:
                t = []
                t.append(value)
            else:
                if self._child:
                    try:
                        t[column] = value
                    except:
                        t.append(value)
                else:
                    try:
                        t[column-1] = value
                    except:
                        t.append(value)

            self.editItem(rowId, values=t)

#======== Getter
    def getItemSelectedRow(self) -> ItemDict:
        iid = self.tree.selection()[0]

        return self.getItem(iid)

    def getValueSelectedColRow(self) -> Any:
        columnId = self._column[1]

        if not self._child: columnId = columnId-1

        v = self.getItemSelectedRow()["values"]

        for i, val in enumerate(v):
            if i == columnId:
                return val

    def getSelectedRow(self) -> tuple:
        return self.tree.selection()

    def getItems(self) -> dict[str, PItemDict]:
        childsIidList = self.__getSubChildren()

        children: dict[str, PItemDict] = {}

        for iid in childsIidList:

            temp: PItemDict = {}

            item: ItemDict = self.getItem(iid)

            temp["values"] = item["values"]
            temp["image"] = item["image"]
            temp["open"] = item["open"]
            temp["tags"] = item["tags"]
            temp["parent"] = None

            parentIID = self.tree.parent(iid)

            if parentIID != "":
                temp["parent"] = parentIID
            
            children[iid] = temp
        
        return children

    def getParentsIID(self, iid: str) -> list[str]:

        parentList = []

        while iid != '':
            parentList.append(iid)
            iid = self.tree.parent(iid)
        return parentList

    def getItem(self, iid: str) -> ItemDict:

        item = self.tree.item(iid)

        newItem: ItemDict = {}

        if self._child:
            t: list = item["values"]
            t.insert(0, item["text"])
        else:
            t = item["values"]

        newItem["values"] = t
        newItem["image"] = item["image"]
        newItem["open"] = item["open"]
        newItem["tags"] = item["tags"]

        return newItem

#======== Action
    def moveUpSelectedItem(self) -> None:
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)-1)

    def moveDownSelectedItem(self) -> None:
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)+1)

#======== Is
    def isSelect(self) -> bool:
        return self.tree.selection().__len__() > 0

    def isEmptyRow(self, iid: str) -> bool:

        i = self.getItem(iid)

        v = len("".join(i["values"]))

        if v == 0:
            return True

        return False

#=======================================================================================================================================================

class Treeview_up(_BaseTreeView):

    def __init__(self, master=None, scroll:Scroll=None, child:bool=False, selectmode: Literal['extended', 'browse', 'none']="browse", indent: int=10, resizeColumn: bool=True, editRow: bool=False, **kw) -> "Treeview_up":

        _BaseTreeView.__init__(self, master=master, scroll=scroll, child=child, selectmode=selectmode, indent=indent, resizeColumn=resizeColumn, editRow=editRow, **kw)

        self.tree.configure(show="tree headings")

    def setColumns(self, columns: list[str], anchor: list[str] = None, stretch: list[bool] = None, minSize: list[int] = None, size: list[int] = None) -> None:

        if self._child:

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

            self.tree.heading("#0", text=columns.pop(0))
            self.tree['columns'] = columns
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


#=======================================================================================================================================================

class Listview_up(_BaseTreeView):

    def __init__(self, master=None, scroll:Scroll=None, child:bool=False, selectmode: Literal['extended', 'browse', 'none']="browse", indent: int=10, editRow: bool=False, **kw) -> "Listview_up":

        _BaseTreeView.__init__(self, master=master, scroll=scroll, child=child, selectmode=selectmode, indent=indent, resizeColumn=False, editRow=editRow, **kw)

        self.tree.configure(show="tree")

    def setColumnsSize(self, size: list[int]) -> None:

        if self._child:

            if size is not None:
                self.tree.column("#0", width=size[0])
                self.tree["column"] = ["#"+str(i) for i in range(1, len(size))]
                for i, col in enumerate(self.tree["column"]):
                    self.tree.column(col, width=size[i+1])

        else:
            if size is not None:
                self.tree.column("#0", width=0, stretch=NO)
                self.tree["column"] = ["#"+str(i) for i in range(1, len(size)+1)]
                for i, col in enumerate(self.tree["column"]):
                    self.tree.column(col, width=size[i])


class _EntryPopup(Entry_up):

    tv: Treeview_up | Listview_up

    def __init__(self, parent, iid, value, colum: int, **kw) -> "_EntryPopup":
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = colum

        self.insert(0, value if value is not None else "")
        # self['state'] = 'readonly'
        # self['readonlybackground'] = 'white'
        # self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", self.on_escape)
        self.bind("<FocusOut>", self.on_return)

    def on_return(self, event) -> None:

        t = self.get()
        self.tv.editValueColRow(t, self.col, self.iid)
        self.destroy()

    def on_escape(self, event) -> None:
        self.check()
        self.destroy()

    def select_all(self, *ignore) -> Literal["break"]:
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'

    def check(self, *ignore) -> None:

        if self.tv.isEmptyRow(self.iid):
            self.tv.removeItem(self.iid)

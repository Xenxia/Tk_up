import tkinter
from typing import Any, Literal, Tuple
from tkinter import ttk
from tkinter.constants import BOTTOM, END, HORIZONTAL, NO, RIGHT, VERTICAL, X, Y, YES

from tk_up.widgets.w import Widget_up
from tk_up.widgets import SCROLL_ALL, SCROLL_X, SCROLL_Y

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

    def __update(self, event):
        pass

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

    def editSelectedElement(self, text:str=None, image=None, values:list|Literal['']=None, open:bool=False, tags:str|list[str]|tuple[str, ...]=None):
        item = self.tree.focus()
        if text != None:
            self.tree.item(item, text=text)
        
        if image != None:
            self.tree.item(item, image=image)

        if values != None:
            self.tree.item(item, values=values)

        if open:
            self.tree.item(item, open=open)

        if tags != None:
            self.tree.item(item, tags=tags)

    def editElement(self, item:str, text:str=None, image=None, values:list|Literal['']=None, open:bool=False, tags:str|list[str]|tuple[str, ...]=None) -> None:
        if text != None:
            self.tree.item(item, text=text)
        
        if image != None:
            self.tree.item(item, image=image)

        if values != None:
            self.tree.item(item, values=values)

        if open:
            self.tree.item(item, open=open)

        if tags != None:
            self.tree.item(item, tags=tags)

    def getItemSelectedElemnt(self, option:str='values') -> Any | None:
        item = self.tree.focus()

        if self.__child and option == "values":
            listValues: list = []
            listValues.append(self.tree.item(item, "text"))
            for value in self.tree.item(item, "values"):
                listValues.append(value)
            return listValues

        result = self.tree.item(item, option)

        if len(self.tree.item(item, option)) == 0:
            result = None

        return result

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


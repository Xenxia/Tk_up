from tkinter import Text, ttk, Pack, Grid, Place
from tkinter.constants import BOTH, END, LEFT, RIGHT, Y

from tk_up.widgets.w import Widget_up, UpdateWidget

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


class Text_up(Text, Widget_up, UpdateWidget):

    def __init__(self, master=None, cnf={}, **kw):
        Text.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)

class ScrolledText_up(ScrolledText, Widget_up, UpdateWidget):

    def __init__(self, master=None, cnf={}, **kw) -> None:
        ScrolledText.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)

class Terminal_ScrolledText_up(ScrolledText, Widget_up, UpdateWidget):

    def __init__(self, master=None, cnf={}, **kw):
        ScrolledText.__init__(self, master=master, cnf=cnf, **kw)
        Widget_up.__init__(self)
        UpdateWidget.__init__(self)

        self.bind("<Key>", lambda e: self.__ctrlEvent(e))
        self.lastIndex: str = "1.0"
        self.lastId: str | None = None
        self.lineId_Index: dict[str, list[str, str, int]] = {}

        self.configTag({
            "Black": ["", "#000000"],
            "White": ["", "#FFFFFF"]
        })

    def __ctrlEvent(self, event) -> None:
        if(12==event.state and event.keysym=='c' ):
            return
        else:
            return "break"

    def configTag(self, tag: dict):
        for key, value in tag.items():
            self.tag_configure(key, background=value[0], foreground=value[1])

    def printLastIndex(self, *texts, color: list = None) -> None:

        if color == None:
            color = ["Black"] * len(texts)

        for index, text in enumerate(texts):
            self.insert(END, text, color[index])

        self.see(END)

    def printLastLine(self, *texts, color: list = None, newLine: bool = True) -> None:

        if color == None:
            color = ["Black"] * len(texts)

        for index, text in enumerate(texts):
            if text == texts[-1]:
                if newLine:
                    self.insert(END, text+"\n", color[index])
                    break

            self.insert(END, text, color[index])

        self.see(END)

    def printSameLine(self, id: str, *texts, color: list = None, newLine: bool = True, update_index: bool = False, see_end: bool = True) -> "Terminal_ScrolledText_up":

        if color == None:
            color = ["Black"] * len(texts)

        texts = list(reversed(texts))
        color = list(reversed(color))

        try:

            if id in self.lineId_Index.keys() and self.lineId_Index[id][2] != 0:
                self.delete(self.lineId_Index[id][0], self.lineId_Index[id][1])

            if not id in self.lineId_Index.keys() or update_index:
                sIndex = self.index("end linestart-1l")
                self.lineId_Index[id] = [sIndex, self.index(sIndex+" lineend"), 0]

            for index, text in enumerate(texts):

                    self.insert(self.lineId_Index[id][0], text, color[index])
                    self.lineId_Index[id][1] = self.index(self.lineId_Index[id][0]+" lineend")

            self.lineId_Index[id][1] = self.index(self.lineId_Index[id][0]+" lineend")

            if newLine and self.lineId_Index[id][2] == 0:
                self.insert(self.lineId_Index[id][1], "\n")

            self.lineId_Index[id][2] += 1

            if see_end:
                self.see(END)
            else:
                self.see(self.lineId_Index[id][1])
        except KeyError as e:
            pass

        return self

    def updateId_Index(self, id: str) -> None:
        if id in self.lineId_Index.keys():
            self.lineId_Index[id] = [self.index("end-1l"), self.index("end+1c"), 0]

    def deleteId_Index(self, id: str) -> None:
        if id in self.lineId_Index.keys():
            self.lineId_Index.pop(id)

    def deletesId_Index(self, ids: list[str]) -> None:

        for id in ids:
            if id in self.lineId_Index.keys():
                self.lineId_Index.pop(id)

    def clearTerminal(self) -> None:
        self.delete("1.0","end")
        self.lineId_Index = {}

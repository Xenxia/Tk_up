from tkinter import *

from tk_up.widgets.view import Listview_up, Treeview_up
from tk_up.widgets.button import Button_up

from tk_up.enum import Scroll
from threading import Thread
from time import sleep

root = Tk()
root.geometry("700x600")


treeView = Listview_up(root, scroll=Scroll.Y, child=False, editRow=True, width=700, height=300)
# treeView.bind("<ButtonRelease-1>", self.selected)
treeView.gridPosSize(row=2, column=0, sticky=(E, W, S, N)).show()
treeView.setColumnsSize([200, 150, 300])
treeView.setTags((
    {
    "name": "Disable",
    "fg": "#F70000",
    },
    {
    "name": "SysDisable",
    "bg": "#AA0000",
    },
))


treeView.addItem(values=["test1", "test2", "test3"])
treeView.addItem(values=["test2","", "test"])
treeView.addItem(parent="1", values=["test","tets2"])
treeView.addItems({"test":{
    "parent": "1",
    "values": ["test", "2", "g"]
}})


treeView2 = Treeview_up(root, scroll=Scroll.ALL, child=True, editRow=True, resizeColumn=False, width=700, height=300)
# treeView.bind("<ButtonRelease-1>", self.selected)
treeView2.gridPosSize(row=3, column=0, sticky=(E, W, S, N)).show()
treeView2.setColumns(
    columns=["test1", "test2", "test3"],
    size=[200, 150, 300]
)
treeView2.setTags((
    {
    "name": "Disable",
    "fg": "#F70000",
    },
    {
    "name": "SysDisable",
    "bg": "#AA0000",
    },
))


treeView2.addItem(values=["test1", "test2", "test3"])
treeView2.addItem(values=["test2","", "test"])
treeView2.addItem(parent="1", values=["test","tets2"])
treeView2.addItems({"test":{
    "parent": "1",
    "values": ["test", "2", "g"]
}})

print(treeView2.getItem("0"))

b = Button_up(root, text="Add Row", command=treeView.addEmptyRow).gridPosSize(row=0, column=0).show()


root.mainloop()
from tkinter import *

from tk_up.widgets.treeview import Treeview_up
from tk_up.widgets import SCROLL_ALL
from threading import Thread
from time import sleep

root = Tk()
root.geometry("700x600")


treeView = Treeview_up(root, scroll=SCROLL_ALL, iid=False, child=True, show="tree headings", editRow=True, width=700, height=300)
# treeView.bind("<ButtonRelease-1>", self.selected)
treeView.gridPosSize(row=2, column=0, sticky=(E, W, S, N)).show()
treeView.setColumns(
    columns=[
        'UI.EDIT_MENU.col_name_profil',
        'UI.EDIT_MENU.col_folder',
        'UI.EDIT_MENU.col_extention'
    ], 
    size=[200, 150, 300]
)
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


treeView.addElement(values=["test","", "test"])
treeView.addElement(values=["test2","", "test"])
treeView.addElement(parent="1", values=["test","tets2"])

root.mainloop()
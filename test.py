from tkinter import *

from tk_up.widgets import Terminal_ScrolledText_up
from threading import Thread
from time import sleep

root = Tk()
root.geometry("400x300")


def delete_text():
    for i in range(5):
        sleep(1)
        Tbox.printSameLine("t", "test :"+str(i))

Tbox = Terminal_ScrolledText_up(root, width=40, height=10)
Tbox.pack()

Tbox.printLastLine("test")


# Tbox.write("write\n")




Button(root, text="delete", command=lambda: Thread(target=delete_text).start()).pack()

root.mainloop()
from tkinter import *

from tk_up.widgets import Terminal_ScrolledText_up
from threading import Thread
from time import sleep

root = Tk()
root.geometry("400x300")


def delete_text():
    for i in range(10):
        sleep(0.1)
        Tbox.printSameLine("t", "test :"+str(i))

def delete_text2():
    for i in range(5):
        sleep(1)
        Tbox.printSameLine("t2", "test :"+str(i))
    
    Tbox.deleteId_Index("t2")

Tbox = Terminal_ScrolledText_up(root, width=40, height=10)
Tbox.pack()

Tbox.printLastLine("test")
Tbox.printLastLine("test")
Tbox.printLastLine("test")
Tbox.printLastLine("test")


# Tbox.write("write\n")




Button(root, text="test", command=lambda: Thread(target=delete_text).start()).pack()
Button(root, text="test2", command=lambda: Thread(target=delete_text2).start()).pack()
Button(root, text="delete", command=lambda: Tbox.delete("2.0", "3.0")).pack()
Button(root, text="insert", command=lambda: Tbox.printLastLine("test")).pack()
Button(root, text="index", command=lambda: print(Tbox.index("end linestart"))).pack()

root.mainloop()
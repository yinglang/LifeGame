
# coding=utf-8
# ! https://docs.python.org/zh-cn/3/library/tkinter.html#a-simple-hello-world-program

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # how it is to behave when the main application window is resized
        self.pack(expand=1)  
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(master=self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(expand=1)

        self.quit = tk.Button(self, text="QUIT", fg="red", bg='black',
                        command=self.master.destroy if self.master is not None else self.destroy)
        self.quit.pack(side="bottom")  # defaults to side = "top"
        # 对内padding的像素，A pixel distance - designating internal padding on each side of the slave widget
        self.quit.pack(ipadx=100, ipady=100)
        # 对外padding的像素，A pixel distance - designating external padding on each side of the slave widget
        self.quit.pack(padx=50, pady=0)

    def say_hi(self):
        print("hi ther, everyone!")

# The Tk class(window manager class) is meant to be instantiated only once in an application,
root = tk.Tk()
# Application programmers need not instantiate one explicitly, the system
#  creates one whenever any of the other classes are instantiated.
# root = None
app = Application(master=root)
app.master.title("Hello World TK")
app.master.maxsize(1000, 400)
app.mainloop()

"""
master-slave is same as parent-child in some GUI API.

tk.Tk:
   tf.Frame (create, attribute, pack(location))
     tf.Button
     tf.Button
"""



# coding=utf-8
# ! https://www.jianshu.com/p/7d81c8432915

from tkinter import Tk, ttk, PhotoImage, Canvas
from tkinter import Menu, StringVar, filedialog, Listbox

class App(Tk):
    def __init__(self):
        super().__init__()
        self._set_scroll()
        self._create_canvas()
        self._scroll_command()
        self._create_button()
        self.canvas.create_window((0, 0), window=self.frame,
                                  anchor='nw')
        self.layout()
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def _set_scroll(self):
        self.scroll_x = ttk.Scrollbar(orient='horizontal')
        self.scroll_y = ttk.Scrollbar(orient='vertical')

    def _create_canvas(self):
        self.canvas = Canvas(width=300, height=100,
                             xscrollcommand=self.scroll_x.set,
                             yscrollcommand=self.scroll_y.set)

    def _scroll_command(self):
        self.scroll_x['command'] = self.canvas.xview
        self.scroll_y['command'] = self.canvas.yview

    def _create_button(self):
        self.frame = ttk.Frame(self.canvas)
        self.button = ttk.Button(self.frame, text="载入图片",
                                 command=self.load_image)

    def layout(self):
        self.button.grid()
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scroll_x.grid(row=1, column=0, sticky="we")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def resize(self, event):
        region = self.canvas.bbox('all')
        self.canvas.configure(scrollregion=region)

    def load_image(self):
        self.button.destroy()
        self.image = PhotoImage(file="python.gif")
        ttk.Label(self.frame, image=self.image).grid()


if __name__ == "__main__":
    app = App()
    app.mainloop()
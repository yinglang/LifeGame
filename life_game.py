import tkinter as tk
import time
from threading import Thread
from queue import Queue

"""
1. use tkinter as GUI, use origin python do it
   Button cost too much resource, will be very slow when world height and world width are large.
   Canvas with Rectangle get better / canvas with rectangle pool.
   Event
2. use sparse array
2. use cython
3. use numpy
"""

class Config(object):
    H = 50  # world height
    W = 100  # world width
    ALIVE_COUNT_RANGE = (3, 3)
    KEEP_RANGE = (2, 2)
    R = 1  # neighbour is (2R+1)*(2R+1)

    ## visulize config
    C = 14   # cell size
    ALIVE_COLOR = 'green'
    DEAD_COLOR = 'white'

class Application(tk.Frame):
    
    def __init__(self, cfg: Config, game, master=None):
        super(Application, self).__init__(master)
        self.master = master
        self.pack(expand=1)
        self.cfg = cfg
        self.game = game
        self.start = False
        self.create_widgets(cfg, self)
        self.has_destroyed = False

    def create_widgets(self, cfg, master):
        width, height = (cfg.W + 2) * cfg.C, (cfg.H + 2) * cfg.C
        self.canvas = canvas = tk.Canvas(master, width=width, height=height)
        canvas.bind("<ButtonRelease-1>", self.canvas_click)
        canvas.pack()
        for h in range(1, 1+cfg.H):
            for w in range(1, 1+cfg.W):
                rect_id = canvas.create_rectangle(w * cfg.C, h * cfg.C, (w+1)*cfg.C, (h+1)*cfg.C, 
                    fill=cfg.ALIVE_COLOR if self.game.get_state(h-1, w-1) else cfg.DEAD_COLOR)

        self.start_button = bt = tk.Button(master)
        bt["text"] = "start"
        bt["command"] = self.start_button_click
        bt.pack()

    def canvas_click(self, event):
        w, h = int(event.x / self.cfg.C) - 1, int(event.y / self.cfg.C) - 1
        if w >= cfg.W or w < 0 or h >= cfg.H or h < 0:
            return
        self.reverse_state([(h, w)])
    
    def start_button_click(self):
        if self.start:
            self.start_button["text"] = "start"
        else:
            self.start_button["text"] = "stop"
        self.start = not self.start

    def reverse_state(self, rect_ids):
        for h, w in rect_ids:
            rect_id = h * cfg.W + w + 1
            color = cfg.DEAD_COLOR if self.game.get_state(h, w) else cfg.ALIVE_COLOR # reverse color
            self.game.set_state(h, w, not self.game.get_state(h, w))
            self.canvas.itemconfig(rect_id, fill=color)

    def main_loop(self, fps=10):
        self.master.update()
        q = Queue()
        self.thread = Thread(target=self.update_graphic, args=(q, ))
        self.thread.start()
        while not self.has_destroyed:
            tic = time.time()
            while q.qsize() > 0:
                change_rect_ids = q.get()
                self.reverse_state(change_rect_ids)
            self.master.update()
            toc = time.time()
            t = 1/fps - (toc -tic)
            if t > 0:
                time.sleep(t)
    
    def update_graphic(self, q:Queue):
        cfg = self.cfg
        print("start runing")
        while not self.has_destroyed:
            if q.qsize() == 0 and self.start:
                changed_rect_ids = []
                state_change = self.game.update_state_change()
                for h in range(cfg.H):
                    for w in range(cfg.W):
                        if state_change[h][w]:
                            changed_rect_ids.append((h, w))
                q.put(changed_rect_ids)
                time.sleep(1)

    def destroy(self):
        super(Application, self).destroy()
        self.has_destroyed = True


class LifeGame(object):

    def __init__(self, cfg):
        self.states = []
        self.states_change = []
        for h in range(cfg.H + 2*cfg.R):
            self.states.append([False] * (cfg.W + 2*2*cfg.R))
            if h >= 2*cfg.R: self.states_change.append([False] * (cfg.W))
        self.cfg = cfg

    def set_state(self, h, w, state):
        self.states[h+self.cfg.R][w+self.cfg.R] = state

    def get_state(self, h, w):
        return self.states[h+self.cfg.R][w+self.cfg.R]

    def update_state_change(self):
        cfg = self.cfg
        states, states_change = self.states, self.states_change

        # clear state change
        for h in range(cfg.H):
            for w in range(cfg.W):
                states_change[h][w] = False

        # cal alive_count
        for h in range(cfg.R, cfg.H+cfg.R):
            for w in range(cfg.R, cfg.W+cfg.R):
                count = 0
                for i in range(-cfg.R, cfg.R+1):
                    for j in range(-cfg.R, cfg.R+1):
                        count += states[h+i][w+j]
                count -= states[h][w]

                # set state_change by count
                if cfg.ALIVE_COUNT_RANGE[0] <= count <= cfg.ALIVE_COUNT_RANGE[1]:
                    if not states[h][w]:  # dead -> alive
                        states_change[h-cfg.R][w-cfg.R] = True
                elif cfg.KEEP_RANGE[0] <= count <= cfg.KEEP_RANGE[1]:
                    pass
                else:
                    if states[h][w]:  # alive -> dead
                        states_change[h-cfg.R][w-cfg.R] = True

        return states_change

    def print_2dlist(self, list2d):
        print()
        for list1d in list2d:
            print(list1d)
        print()


root = tk.Tk()
root.title("Life Game")
cfg = Config()
game = LifeGame(cfg)
app = Application(cfg, game, root)
app.main_loop()

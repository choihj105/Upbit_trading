import tkinter as tk
from tkinter.constants import BOTH
from .V1 import mainView as W1
from .V2 import subView as W2

## View
class View(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # mainView Init        
        self.main = W1.View_main(master)
        self.main.pack(fill = BOTH, expand= True)
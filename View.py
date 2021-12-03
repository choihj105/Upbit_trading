import tkinter as tk
from tkinter.constants import BOTH
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import View_main

## View

class View(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        main = View_main.View_main(master) # root 경로를 이어준다
        main.pack(fill = BOTH, expand= True)
        


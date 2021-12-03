import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import View

import requests
import pyupbit
import pprint
import time
import datetime
import math
import queue
import threading


# GUI Main loop
class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        config = {"title":"UPBIT 자동매매 프로그램", "version":"[Version: 0.1]"}
        self.title(config["title"] + " " + config["version"])                     # Title 창 이름 변경
        
        # iconPath = "./Source/healthIcon.ico"
        # root.iconbitmap(default = iconPath)     # Title 창 아이콘 변경
        self.geometry("640x550")
        self.resizable(True, True)
        self.configure(bg='snow')
        

        #main = view_test.View_main()
        View.View(self)
        
        
        
        

app = Main()
app.mainloop()
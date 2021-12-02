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

# Main Loop


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UPBIT 자동매매 프로그램")
        self.geometry("640x550")
        self.resizable(False, False) # x(너비), y(높이) 값 변경 불가(창 크기 변경 불가)
        
        View.View(self)


if __name__ == "__main__":
    root = Main()
    root.mainloop()
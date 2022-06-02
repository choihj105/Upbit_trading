import tkinter as tk
from tkinter.constants import BOTH
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import View_main
import View_subMain

## View
class View(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # mainView Init        
        self.main = View_main.View_main(master)
        self.main.pack(fill = BOTH, expand= True)

        # subView Init
        window = tk.Toplevel(master)
        self.subMain = View_subMain.View_main(window) # need 안보이게 하는 기능 추가

        # mainView Func
        self.main.btn_add_func.bind("<Button-1>", self.pack) # need 보이게 하는 기능 추가
        
        # subView Func
        self.subMain.btn_ok.bind("<Button-1>", self.Add_Confirm)
    
    def pack(self, event):
        self.subMain.pack(fill = BOTH, expand= True)


    # 확인 버튼 함수
    def Add_Confirm(self, event):
        mm_txt = []
        mm_txt = [self.subMain.cmb_type.get(), self.subMain.cmb_amount.get(), self.subMain.buy_e.get(), self.subMain.sell_e.get(), self.subMain.stoploss_e.get()]
        self.main.standby_list.insert(tk.END, mm_txt)
        


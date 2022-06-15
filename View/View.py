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

        # subView Init
        #window = tk.Toplevel(master)
        #self.subMain = W2.View_main(window) # need 안보이게 하는 기능 추가

        # mainView Func
        #self.main.func_frame.btn1.bind("<Button-1>", self.Add_Ticker) # need 보이게 하는 기능 추가

        # subView Func
        #self.subMain.btn_ok.bind("<Button-1>", self.Add_Confirm)
    
    # Main 화면에서 추가 버튼을 누를 시
    #def Add_Ticker(self, event):
        #self.subMain.pack(fill = BOTH, expand= True)

    # 확인 버튼 함수
    #def Add_Confirm(self, event):
        #mm_txt = []
        #mm_txt = [self.subMain.cmb_type.get(), self.subMain.cmb_amount.get(), self.subMain.buy_e.get(), self.subMain.sell_e.get(), self.subMain.stoploss_e.get()]
        #self.main.standby_list.insert(tk.END, mm_txt)
        


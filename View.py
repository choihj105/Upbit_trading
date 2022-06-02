import tkinter as tk
from tkinter.constants import BOTH
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import View_main
import View_subMain
import pyupbit

## View
class View(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
                
        main = View_main.View_main(master) # root 경로를 이어준다
        main.pack(fill = BOTH, expand= True)

        # mainView Func
        main.btn_add_func.bind("<Button-1>", self.createNewWindow)
        
        # subView Func

    def createNewWindow(self, event):
        window = tk.Toplevel(self.master)
        #window.geometry()
        self.transWindow = View_subMain.View_main(window)
        self.transWindow.pack(fill = BOTH, expand=True)
        
    def printCurPrice():
        # 마켓 코드(이름)
        upbit_krw_tickers = pyupbit.get_tickers(fiat="KRW")
        # 코인의 현재가 / 튜블형식
        upbit_cur_price = pyupbit.get_current_price(upbit_krw_tickers)
        return upbit_cur_price


    # 확인 버튼 함수
    def Add_Confirm(self):
        mm_txt = []
        mm_txt = [self.cmb_type.get(), self.cmb_amount.get(), self.buy_e.get(), self.sell_e.get(), self.stoploss_e.get()]
        self.master.standby_list.insert(END, mm_txt)


import tkinter as tk
from tkinter.constants import BOTH, TOP
from . import orderF1
from ..V2 import subView as W2

class View_main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.in_list_frame = orderF1.orderFrame(self, text="진행중인 주문") # 매매진행 리스트 프레임
        self.standby_list_frame = orderF1.orderFrame(self, text="대기중인 주문") # 매매대기 리스트 프레임
        self.func_frame = orderF1.funcFrame(self, n1 = "추가", n2 = "삭제") # 기능 프레임1(추가, 삭제)
        self.func_frame2 = orderF1.funcFrame(self, n1= "실행", n2= "실행취소") # 기능 프레임2 (실행, 실행취소버튼)
        self.func_frame3 = orderF1.funcFrame(self, n1="자동매수", n2="자동매수취소")  # 기능 프레임3 (자동매수, 자동매수취소버튼 )
        self.cur_asset_frame = orderF1.currencyFrame(self) # 주문가능한 현재자산 프레임

        # Packing
        self.in_list_frame.pack(fill="both", expand=True, padx=5, pady=5, ipady=5)
        self.standby_list_frame.pack(fill="both", expand=True, padx=5, pady=5, ipady=5)
        self.func_frame.pack(fill="both", padx=5, pady=5)
        self.func_frame2.pack(fill="both", padx=5, pady=5)
        self.func_frame3.pack(fill="both", padx=5, pady=5)
        self.cur_asset_frame.pack(fill="both", padx=5, pady=5, ipady=10, ipadx=10)

        # Function
        self.func_frame.btn1.bind("<Button-1>", self.Add_Ticker) # need 보이게 하는 기능 추가
        self.func_frame.btn2.bind("<Button-1>", self.Del_Ticker)
        #self.subMain.okcnl_frame.bind("<Button-1>", self.Add_Confirm)
    
    def Add_Ticker(self, event):
        window = tk.Toplevel(self)
        self.subMain = W2.View_main(window)
        self.subMain.pack(fill = BOTH, expand= True)

    def Del_Ticker(self, event):
        for index in reversed(self.standby_list_frame.in_list.curselection()):   # 리스트박스에 클릭한 것을 순서를 출력해주고 그것을 리버스로 반환함
            self.standby_list_frame.in_list.delete(index)

    def Add_Confirm(self, event):
        mm_txt = []
        mm_txt = [self.subMain.request_frame.cmb_type.get(), self.subMain.request_frame.cmb_amount.get(),\
            self.subMain.buy_frame.e.get(), self.subMain.sell_frame.e.get(), self.subMain.stoploss_frame.e.get()]
        self.standby_list_frame.in_list.insert(tk.END, mm_txt)
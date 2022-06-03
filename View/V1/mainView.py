import tkinter as tk
from tkinter.constants import BOTH, TOP
from . import orderF1

class View_main(tk.Frame):
    from . import mainFunc

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

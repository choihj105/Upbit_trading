import tkinter as tk
from . import orderF2

class View_main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 주문 프레임 (1-3)
        self.request_frame = orderF2.orderFrame(self, text="주문")
        # 매수 프레임 (4)
        self.buy_frame = orderF2.costFrame(self, text="매수")
        # 매도 프레임 (5)
        self.sell_frame = orderF2.costFrame(self, text="매도")
        # 손절 프레임 (6)
        self.stoploss_frame = orderF2.costFrame(self, text="손절")
        # 확인_취소 프레임 (7)
        self.okcnl_frame = orderF2.funcFrame(self, n1="확인", n2="취소")

        # Packing
        self.request_frame.pack(padx=5, pady=5, ipady=5)
        self.buy_frame.pack(padx=5, pady=5, ipady=5, fill="x")
        self.sell_frame.pack(padx=5, pady=5, ipady=5, fill="x")
        self.stoploss_frame.pack(padx=5, pady=5, ipady=5, fill="x")
        self.okcnl_frame.pack(padx=5, pady=5, ipady=5, fill="x")

        self.buy_frame.cost.set(self.request_frame.cur_price_label.cget('text'))
        
        # Function     
        self.buy_frame.cmb.bind("<<ComboboxSelected>>", \
            lambda event, a= self.request_frame, b=self.buy_frame:
            self.Conv(event,a,b))
        
        self.sell_frame.cmb.bind("<<ComboboxSelected>>", \
            lambda event, a= self.buy_frame, b=self.sell_frame:
            self.Conv(event,a,b))

        self.stoploss_frame.cmb.bind("<<ComboboxSelected>>", \
            lambda event, a= self.buy_frame, b=self.stoploss_frame:
            self.Conv(event,a,b))


    def Conv(self, event, a , b):
        cost = a.cost.get()
        if b.cmb.get() == "직접입력":
            pass
        else:
            rate = b.cmb.get()[:-1]
            cur_price = cost
            b.e.delete("0", tk.END)
            b.e.insert(0, orderF2.Change(cur_price, rate))
            b.cost.set(b.e.get())
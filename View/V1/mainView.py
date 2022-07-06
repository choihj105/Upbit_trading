import tkinter as tk
import tkinter.messagebox as msgbox
import pyupbit
from tkinter.constants import BOTH, TOP
from . import orderF1
from ..V2 import subView as W2

class View_main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.upbit = self.__Account_Init()
        
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
        self.__Update_currency()
        self.func_frame2.btn1.bind("<Button-1>", self.Check_Price)
    
    def __Account_Init(self):
        # access key와 secret key를 발급
        f = open("C:/Users/호준/Desktop/upbitkey.txt")
        lines = f.readlines()
        access = lines[0].strip()
        secret = lines[1].strip()
        f.close()
        
        # 업비트 exchange APi를 위하여 객체만듬
        upbit = pyupbit.Upbit(access, secret)
        return upbit

    def __Update_currency(self):
        cur_krw_balances = self.upbit.get_balance("KRW")
        self.cur_asset_frame.cur_asset_label.configure(text=cur_krw_balances)
        self.after(3000, self.__Update_currency)

    def Add_Ticker(self, event):
        window = tk.Toplevel(self)
        self.subMain = W2.View_main(window)
        self.subMain.pack(fill = BOTH, expand= True)
        self.subMain.okcnl_frame.btn1.bind("<Button-1>", self.Add_Confirm)

    def Del_Ticker(self, event):
        for index in reversed(self.standby_list_frame.in_list.curselection()):   # 리스트박스에 클릭한 것을 순서를 출력해주고 그것을 리버스로 반환함
            self.standby_list_frame.in_list.delete(index)

    def Add_Confirm(self, event):
        mm_txt = []
        mm_txt = [self.subMain.request_frame.cmb_type.get(), self.subMain.request_frame.cmb_amount.get(),\
            self.subMain.buy_frame.e.get(), self.subMain.sell_frame.e.get(), self.subMain.stoploss_frame.e.get()]
        self.standby_list_frame.in_list.insert(tk.END, mm_txt)

    #################
    # Check_Price -> (예약주문)매수 , Check_Price -> (현재진행중인)매도

    def Check_Price(self, event):
        size = self.standby_list_frame.in_list.size() # 확인해보려는 코인 개수
        coins = self.standby_list_frame.in_list.get(0, size)

        if size == 0:
            # error!
            self.after(100, orderF1.my_Msg.info_error)
            return

        for i in coins:
            coin_ticker = "KRW-"+ i[0] # 코인 종류
            buy_target = float(i[2]) # 매수 목표가
            cur_price = float(pyupbit.get_current_price(coin_ticker))

            if cur_price >= buy_target:
                # 매수 함수
                self.after(10, self.Start_Buy(i))
                return
        
        self.after(1000, self.Check_Price)
        
    def Start_Buy(self, coin):
        coin_ticker = "KRW-"+ coin[0] # 코인 종류
        buy_percent = coin[1] # 남은 가격 매수 퍼센트

        krw_balance = self.upbit.get_balance("KRW")
        buy_percent = float(buy_percent[:-1]) / 100
        coin_balance = krw_balance * buy_percent
        coin_balance = round(coin_balance, -3)

        if(coin_balance <= 5000 or krw_balance <= 5000):
            self.after(100, orderF1.my_Msg.info_error3)
            return

        #self.upbit.buy_market_order(coin_ticker, krw_balance)
        tmp = coin + (coin_balance, round(coin_balance*float(coin[3])/float(coin[2])),\
            round(coin_balance*float(coin[4])/float(coin[2])),)
        
        self.standby_list_frame.in_list.delete(0,tk.END)
        self.in_list_frame.in_list.insert(tk.END, tmp)
        self.after(100, orderF1.my_Msg.info_start)


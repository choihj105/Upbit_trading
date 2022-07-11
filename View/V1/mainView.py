from asyncio.windows_events import NULL
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
        self._jobB =None
        self._jobS =None
        self._jobAuto =None
        self._Auto_Base_Price =None

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
        self.__Update_currency()
        self.func_frame.btn1.bind("<Button-1>", self.Add_Ticker) # need 보이게 하는 기능 추가
        self.func_frame.btn2.bind("<Button-1>", self.Del_Ticker)
        self.func_frame2.btn1.bind("<Button-1>", self.Check)
        self.func_frame2.btn2.bind("<Button-1>", self.Cancle)
        self.func_frame3.btn1.bind("<Button-1>", self.AutoCheck)
        self.func_frame3.btn2.bind("<Button-1>", self.AutoCancle)
    
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
    def Check(self, event):
        B_size = self.standby_list_frame.in_list.size()
        S_size = self.in_list_frame.in_list.size()
        if(B_size == 0 and S_size == 0):
            self.after(100, orderF1.my_Msg.info_error)
            return

        self.after(100, orderF1.my_Msg.info_start)
        self.Check_S()
        self.Check_B()

    def Cancle(self, event):
        try:
            #if func == 'B':
            if self._jobB != None:
                self.after_cancel(self._jobB)
                self.standby_list_frame.in_switch.config(bg="#FF6666")
                self._jobB = None
            
            #if func == 'S':
            if self._jobS != None:
                self.after_cancel(self._jobS)
                self.in_list_frame.in_switch.config(bg="#FF6666")
                self._jobS = None    

            self.after(100, orderF1.my_Msg.info_cnl)
        
        except:
            self.after(100, orderF1.my_Msg.info_error4)     

    def Check_B(self):
        size = self.standby_list_frame.in_list.size() # 확인해보려는 코인 개수
        coins = self.standby_list_frame.in_list.get(0, size)

        # 매수
        for i in coins:
            coin_ticker = "KRW-"+ i[0] # 코인 종류
            buy_target = float(i[2]) # 매수 목표가
            cur_price = float(pyupbit.get_current_price(coin_ticker))
            print(cur_price)
            if cur_price >= buy_target:
                # 매수 함수
                self.after(10, self.Start_Buy(i))
                return

        self.standby_list_frame.in_switch.config(bg="#66FF66")
        self._jobB = self.after(1000, self.Check_B)
    
    def Check_S(self):
        size = self.in_list_frame.in_list.size() # 확인해보려는 코인 개수
        coins = self.in_list_frame.in_list.get(0, size)

        if size > 0:
            # 매도
            for i in coins:
                coin_ticker = "KRW-"+ i[0] # 코인 종류
                sell_target = float(i[3]) # 매도 목표가
                stoploss_taget = float(i[4]) # 손절 목표가
                cur_price = float(pyupbit.get_current_price(coin_ticker))

                if cur_price >= sell_target:   # 손절
                    # 매도 함수
                    self.after(10, self.Start_Sell(i, coins.index(i)))
                    return

                if cur_price <= stoploss_taget: # 손절
                    # 매도 함수
                    self.after(10, self.Start_Sell(i, coins.index(i)))
                    return
        
        self.in_list_frame.in_switch.config(bg="#66FF66")       
        self._jobS = self.after(1000, self.Check_S)
    
    # 시장가 매수, 나중에 지정가로 바꿀 예정
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
        self.standby_list_frame.in_switch.config(bg="#FF6666")
        self.after(100, orderF1.my_Msg.info_buy)

    # 시장가 매도, 나중에 지정가로 바꿀 예정
    def Start_Sell(self, coin, idx):
        coin_ticker = "KRW-"+ coin[0] # 코인 종류
        coin_balance = self.upbit.get_balance(coin_ticker) # 내가 산 코인 수량
        
        self.after(100, orderF1.my_Msg.info_sell)
        # self.upbit.sell_market_order(coin_ticker, coin_balance)
        self.in_list_frame.in_list.delete(idx)
        self.in_list_frame.in_switch.config(bg="#FF6666")

    ########## 
    # 자동매매
    def AutoCancle(self, event):
        try:
            #if func == 'Auto':
            if self._jobAuto != None:
                self.after_cancel(self._jobAuto)
                self._jobAuto = None
                self._Auto_Base_Price = None
            self.after(100, orderF1.my_Msg.info_auto_cnl)
        except:
            self.after(100, orderF1.my_Msg.info_error4) 


    def AutoCheck(self, event):
        tickers = pyupbit.get_tickers(fiat="KRW")

        # 시작 했을때의 가격 기준점
        if self._Auto_Base_Price == None:
            self.after(100, orderF1.my_Msg.info_auto)
            self._Auto_Base_Price = pyupbit.get_current_price(tickers)

        # 갱신되는 가격
        Cur_Dict = pyupbit.get_current_price(tickers)
        Cur_Prices = list(Cur_Dict.values())
        Cur_Tickers = list(Cur_Dict.keys())

        # 기존 가격
        Base_Prices = list(self._Auto_Base_Price.values())

        for i in range(len(Cur_Dict)):
            if  Cur_Prices[i] >= (Base_Prices[i] * 1.05):
                print(Cur_Tickers[i], ": ", Cur_Prices[i], Base_Prices[i])

                # 자동 매수
                order = orderF1.my_Msg.ask_auto_buy(Cur_Tickers[i], Cur_Prices[i]) # yes, no
                if order == 'yes':
                    # 매수
                    print(Cur_Tickers[i] + " 매수하였습니다.")
                    coin_ticker = Cur_Tickers[i]
                    krw_balance = self.upbit.get_balance("KRW")
                    krw_balance *= 0.3 # 매수 퍼센트
                    krw_balance = round(krw_balance, -3)

                    try:
                        #self.upbit.buy_market_order(coin_ticker, krw_balance)
                        self.after(100, orderF1.my_Msg.info_buy)
                    except:
                        self.after(100, orderF1.my_Msg.info_error)

                    tmp = [coin_ticker[-3:], "30%", Cur_Prices[i], round(Cur_Prices[i] * 1.1, 1), round(Cur_Prices[i]*0.97, 1),"자동매매진행중"]
                    self.in_list_frame.in_list.insert(tk.END, tmp)
                    self.after(100, self.Check_S)
                    return

        self._jobAuto = self.after(1000, self.AutoCheck, event)



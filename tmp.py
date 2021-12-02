from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import requests
import pyupbit
import pprint
import time
import datetime
import math
import queue
import threading


# 찐찐찐이야

# access key와 secret key를 발급
f = open("C:/Users/호준/Desktop/upbitkey.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

# 업비트 exchange APi를 위하여 객체만듬
upbit = pyupbit.Upbit(access, secret)

# 현재 투자한 자금 출력
upbit_balances = upbit.get_balances()

# 마켓 코드(이름)
upbit_krw_tickers = pyupbit.get_tickers(fiat="KRW")

# 코인의 현재가 / 튜블형식
upbit_cur_price = pyupbit.get_current_price(upbit_krw_tickers)
# print(cur_price)

# 1초마다 현재가를 얻는 함수
#def cur_price(ticker):
#    while True:
#        price = pyupbit.get_current_price(ticker)
#        now = datetime.datetime.now()
#        print(now)
#        print(price)
#        time.sleep(1)

def cur_balances(ticker):
    upbit_balances = upbit.get_balances()
    
    if "KRW" in upbit_balances[0]["currency"]:
        return upbit_balances[0]["balance"]
    else:
        return 0
    

    
def Change(cur_price, rate):
    cur_price = float(cur_price)
    rate = float(rate)
    cur_price += (cur_price * (rate/100))
    
    if cur_price > 0 and cur_price < 10:
        return round(cur_price, 4)
    elif cur_price >= 10 and cur_price <100:
        return round(cur_price, 3)
    elif cur_price >= 100 and cur_price <1000:
        return round(cur_price, 2)
    elif cur_price >= 1000 and cur_price <10000:
        return round(cur_price, 1)
    elif cur_price >= 10000 and cur_price <100000:
        return round(cur_price, 0)
    elif cur_price >= 100000 and cur_price <1000000:
        return round(cur_price, -1)
    elif cur_price >= 1000000 and cur_price <10000000:
        return round(cur_price, -2)
    elif cur_price >= 10000000 and cur_price <100000000:
        return round(cur_price, -3)
    elif cur_price >= 100000000 and cur_price <1000000000:
        return round(cur_price, -4)
    else:
        print("값이 없음")





class Main_pump(Tk):
    def __init__(self):
        
        super().__init__()
        self.title("DCTSS (Digital Currency Trading Support System)") # 타이틀
        self.geometry("640x550")
        self.resizable(False, False) # x(너비), y(높이) 값 변경 불가(창 크기 변경 불가)
        self.op_mode = False
        self.op_mode2 = True
        self.op_mode3 = True
        self.autobuy_op = True
        self.autosell_op = False
        self.hold = False
        self.num = 0
        self.select = []
        
        #  매매진행 리스트 프레임
        in_list_frame = LabelFrame(self, text="진행중인 주문")
        in_list_frame.pack(fill="both", padx=5, pady=5, ipady=5)

        # 매매진행중인 리스트의 스크롤바
        in_scrollbar = Scrollbar(in_list_frame)
        in_scrollbar.pack(side="right", fill="y")

        # 매매진행중인 리스트
        in_list = Listbox(in_list_frame, selectmode="extended", height=8, yscrollcommand=in_scrollbar.set)
        in_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        in_scrollbar.config(command=in_list.yview)


        # 매매대기중인 리스트 프레임
        standby_list_frame = LabelFrame(self, text="대기중인 주문")
        standby_list_frame.pack(fill="both", padx=5, pady=5, ipady=5)

        # 매매대기중인 리스트의 스크롤바
        standby_scrollbar = Scrollbar(standby_list_frame)
        standby_scrollbar.pack(side="right", fill="y")

        # 매매대기중인 리스트
        standby_list = Listbox(standby_list_frame, selectmode="extended", height=8, yscrollcommand=standby_scrollbar.set)
        standby_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)


        # 기능 프레임 (추가, 삭제버튼 )
        func_frame = Frame(self)
        func_frame.pack(fill="both", padx=5, pady=5)

        # 추가버튼
        btn_add_func = Button(func_frame, padx=5, pady=5, width=12, text="추가", command= Main_pump_add)
        btn_add_func.pack(side="left")

        # 삭제버튼
        
        btn_del_func = Button(func_frame, padx=5, pady=5, width=12, text="삭제", command= self.Del_Cancle)
        btn_del_func.pack(side="right")
        
        
        # 기능 프레임2 (실행, 실행취소버튼 )
        func_frame2 = Frame(self)
        func_frame2.pack(fill="both", padx=5, pady=5)

        # 실행버튼
        
        btn_exec_func = Button(func_frame2, padx=5, pady=5, width=12, text="실행", command=self.mul_select)
        btn_exec_func.pack(side="left")

        # 실행취소버튼
        btn_exec_cnl_func = Button(func_frame2, padx=5, pady=5, width=12, text="실행취소", command = self.cnl_mul_select)
        btn_exec_cnl_func.pack(side="right")
        
        
        # 기능 프레임3 (자동매수, 자동매수취소버튼 )
        func_frame3 = Frame(self)
        func_frame3.pack(fill="both", padx=5, pady=5)

        # 자동매수버튼
        
        btn_auto_func = Button(func_frame3, padx=5, pady=5, width=12, text="자동매수", command=self.autoBuy)
        btn_auto_func.pack(side="left")

        # 자동매수취소버튼
        btn_auto_cnl_func = Button(func_frame3, padx=5, pady=5, width=12, text="자동매수취소")
        btn_auto_cnl_func.pack(side="right")
        
        
        
        # 주문가능한 현재자산 프레임
        cur_asset_frame = Frame(self)
        cur_asset_frame.pack(fill="both", padx=5, pady=5, ipady=10, ipadx=10)

        # krw 표시 레이블
        cur_asset_krw_label = Label(cur_asset_frame, text="krw")
        cur_asset_krw_label.pack(side="right")

        # 현재자산 레이블
        cur_krw_balances = upbit.get_balance("KRW")
        cur_asset_label = Label(cur_asset_frame, text=cur_krw_balances, width=15, anchor="e")
        cur_asset_label.pack(side="right")

        # 주문가능 레이블
        cur_asset_txt_label = Label(cur_asset_frame, text="주문가능")
        cur_asset_txt_label.pack(side="right")
        
        self.standby_list = standby_list
        self.in_list = in_list

        
    def info_start(self):
        if self.op_mode is False and self.op_mode2 is True and self.hold is False and self.num == 0:
            msgbox.showinfo("알림", "정상적으로 주문이 접수 되었습니다.")
            self.num += 1
            
    def info_error(self):
        msgbox.showerror("에러", "주문 오류가 발생하였습니다. 주문설정을 해주세요")
    def info_error2(self):
        msgbox.showerror("에러", "주문 오류가 발생하였습니다. 빈값을 확인해주세요")
        
    def info_buy(self):
        msgbox.showinfo("알림", "정상적으로 매수 완료되었습니다.")
    def info_sell(self):
        msgbox.showinfo("알림", "정상적으로 매도 완료되었습니다.")
    def info_cnl(self):
        msgbox.showinfo("알림", "정상적으로 주문이 취소되었습니다.")
    def info_auto(self):
        msgbox.showinfo("알림", "정상적으로 자동매매주문이 접수되었습니다.")
    
    
    def Del_Cancle(self):
        for index in reversed(self.standby_list.curselection()):   # 리스트박스에 클릭한 것을 순서를 출력해주고 그것을 리버스로 반환함
            self.standby_list.delete(index)
        
    
    # 시장가 매수
    def start_buy(self, selected):

        coin_ticker = "KRW-"+ selected[0] # 코인 종류
        buy_percent = selected[1] # 남은 가격 매수 퍼센트
        buy_target = float(selected[2]) # 매수 매표가
        sell_target = float(selected[3]) # 매도 목표가
        stoploss_taget = float(selected[4]) # 손절 
        
        price = pyupbit.get_current_price(coin_ticker) # 코인 현재 가격
        
        # print("(매수)",now, price)
            
        if self.op_mode is True and price is not None and self.hold is False:

            krw_balance = upbit.get_balance("KRW")
            buy_percent = float(buy_percent[:-1]) / 100
            krw_balance *= buy_percent
            krw_balance = round(krw_balance, -3)
            krw_balance -= 1000
            upbit.buy_market_order(coin_ticker, krw_balance)
            #self.info_buy()
            print("매수가 완료 되었습니다")
            
            
            self.hold = True
            self.op_mode= False

    
    # 시장가 매도       
    def start_sell(self,selected):
        
        coin_ticker = "KRW-"+ selected[0] # 코인 종류
        
        buy_target = float(selected[2]) # 매수 매표가
        sell_target = float(selected[3]) # 매도 목표가
        stoploss_taget = float(selected[4]) # 손절
        
        price = pyupbit.get_current_price(coin_ticker) #코인가격
        coin_balance = upbit.get_balance(coin_ticker) # 내가 산 코인 수량
        # print("(매도 중간단계)", price)
        
        
        # 수익 매도
        if self.op_mode is True and price is not None and self.hold is True:
            upbit.sell_market_order(coin_ticker, coin_balance)
        
            self.info_sell()
            print("매도가 완료 되었습니다")
            self.num = 0 
            self.hold = False
            self.op_mode = False
        
        # 손절 매도
        elif self.op_mode is True and price is not None and self.hold is True:
            upbit.sell_market_order(coin_ticker, coin_balance)

            self.info_sell()
            print("손절이 완료 되었습니다")
            self.num = 0
            self.hold = False
            self.op_mode = False

    
    
    # 매수 매도 손절
    def mul_select(self):
        standby_list_index = self.standby_list.size()
        coin_var = self.standby_list.get(0, standby_list_index)
        
        if standby_list_index == 0:
            self.info_error()
            return
        else:
            self.info_start()
        
        
        # 매수 시그널
        if self.hold is False and self.op_mode is False:
            for i in coin_var:
                
                coin_ticker = "KRW-"+ i[0] # 코인 종류
                buy_target = float(i[2]) # 매수 매표가
                coin_current_price = float(pyupbit.get_current_price(coin_ticker))
                
                # print("코인종류: {0} 매수가격: {1} 현재가격: {2}".format(coin_ticker, buy_target, coin_current_price))

                if coin_current_price >= buy_target:
                    self.select = i
                    
                    # 대기중인 주문 다 사라지게
                    self.standby_list.delete(0,END)
                    notice = "현재-" + self.select[0] + "-코인-주문-진행중-입니다."
                    self.standby_list.insert(END, notice)
                    
                    # 진행중인 주문에 넣게
                    self.in_list.insert(END, self.select)
                    
                    
                    # print("매수가격 충족", select)
                    self.op_mode = True
                    self.start_buy(self.select)
                    
                    print(upbit.get_balance("KRW"))
                    
                    break


        # 매도 시그널
        if self.hold is True and self.op_mode is False:
            coin_current_price = float(pyupbit.get_current_price("KRW-"+ self.select[0]))
            sell_target = float(self.select[3]) # 매수 목표가
            stoploss_taget = float(self.select[4]) # 손절 목표가
            # print(f'매도조건: {select} 현재 가격:{coin_current_price}')

            #이익 매도
            if sell_target <= coin_current_price:
                self.op_mode = True
                self.start_sell(self.select)
                
                # 리스트박스 삭제
                self.in_list.delete(0,END)
                self.standby_list.delete(0,END)
                
                self.select = []
                print(upbit.get_balance("KRW"))
                return

            #손절
            elif stoploss_taget >= coin_current_price:
                self.op_mode = True
                self.start_sell(self.select)
                
                # 리스트박스 삭제
                self.in_list.delete(0,END)
                self.standby_list.delete(0,END)
                
                self.select = []
                print(upbit.get_balance("KRW"))
                return
        
        
        if self.op_mode2:
            self.after(2000, self.mul_select)
        else:
            self.info_cnl()
            self.select = []
            self.op_mode2 = True
            return
            
    def cnl_mul_select(self):
        self.op_mode2 = False
        return
    
    
    # 자동매수 함수
    def getInfo(self,ticker):
        if ticker is ETH_df:
            sell_info = [3.99, 17.49]
            return sell_info

        elif ticker is XRP_df:
            sell_info = [17.3, 3.15]
            return sell_info

        elif ticker is XLM_df:
            sell_info = [4.37, 15.61]
            return sell_info

        else:
            return
    def getRedCandle(self,ticker_df):
        open_price = ticker_df['open'][-1]
        close_price = ticker_df['close'][-1]
        
        if open_price <= close_price:
            return True
        else:
            return False

    def getTrendBTC(self,btc_df):

        BTC_cur_price = btc_df["close"][-1]
        BTC_ma60 = btc_df["close"].sum() / 60


        if BTC_cur_price > BTC_ma60:
            return True
        else:
            return False

    def getVolumn(self,ticker_df):
        v_cur_min = ticker_df['volume'][-1]
        v_min_30_avg = ticker_df['volume'][:30].sum() / 30


        if v_cur_min >= v_min_30_avg * 2.5:
            return True
        else:
            return False


    def getStart(self,btc_df, ticker_df):

        if self.getTrendBTC(btc_df) is True and self.getVolumn(ticker_df) is True and self.getRedCandle(ticker_df) is True:
            print("알림")
            return True
        else:
            return False


    def yesnocancle(self):
        response = msgbox.askyesnocancel(title=None, message="매수 하시겠습니까?")
        # 네 : 저장후 종료
        # 아니오 : 저장 하지 않고 종료
        # 취소 : 프로그램 종료 취소 (현재 화면에서 계속 작업)
        print("응답: ", response) # True, False, None 
        if response == 0:
            print("아니오")
        elif response == 1:
            print("예")

            # 시장가 매수

        else:
            print("취소")


    def autoBuy(self):
        if self.op_mode3 is True:
            self.info_auto()
            notice = "현재-[ETH, XRP, XLM]-코인-주문-자동매수진행중-입니다."
            self.in_list.insert(END, notice)
        
        if self.autobuy_op is True:
            BTC_df = pyupbit.get_ohlcv("KRW-BTC", "minute60", 60)  # 업비트에서 최대 200개만 받아 올 수 있음
            ETH_df = pyupbit.get_ohlcv("KRW-ETH", "minute1", 31)  # 업비트에서 최대 200개만 받아 올 수 있음
            XRP_df = pyupbit.get_ohlcv("KRW-XRP", "minute1", 31)  # 업비트에서 최대 200개만 받아 올 수 있음
            XLM_df = pyupbit.get_ohlcv("KRW-XLM", "minute1", 31)  # 업비트에서 최대 200개만 받아 올 수 있음

            ticker_list = [ETH_df, XRP_df, XLM_df]
            for i in ticker_list:
                #name = str(i)
                if self.getStart(BTC_df, i) is True:
                    #print(name)ii
                    #yesnocancle()
                    
                    # 정보 얻기
                    tradingInfo = self.getInfo(i)
                    sell_per, stop_per = tradingInfo
                    
                    if i is ETH_df:
                        coin_ticker = "KRW-ETH"
                    elif i in XRP_df:
                        coin_ticker = "KRW-XRP"
                    elif i in XLM_df:
                        coin_ticker = "KRW-XLM"

                    # 자동 매수
                    krw_balance = upbit.get_balance("KRW")
                    #krw_balance = round(krw_balance, -3)
                    krw_balance = round(krw_balance, -3)
                    krw_balance -= 1000
                    upbit.buy_market_order(coin_ticker, krw_balance)
                    
                    self.in_list.delete(0,END)
                    notice = "현재-" + coin_ticker + "-코인-주문-매도진행중-입니다."
                    self.in_list.insert(END, notice)
                    
                    self.info_buy()
                    
                    # 자동 매도
                    buy_price = pyupbit.get_current_price(coin_ticker)
                    sell_price = buy_price * (1 + sell_per/100)
                    stop_price = buy_price * (1 - stop_per/100)
                    self.autobuy_op = False
                    self.autosell_op = True
        
        self.op_mode3 = False
        if self.autobuy_op is True:
            self.after(2000, self.autoBuy)
        
        else:
            self.autoSell(sell_price, stop_price, coin_ticker)

            
    
    
    # 자동 매도
    def autoSell(self, sell_price, stop_price, coin_ticker):
        
        price = pyupbit.get_current_price(coin_ticker)

        # 이득 매도
        if sell_price <= price:
            coin_balance = upbit.get_balance(coin_ticker) # 내가 산 코인 수량 
            upbit.sell_market_order(coin_ticker, coin_balance)
            
            self.in_list.delete(0,END)
            self.info_sell()
            
            self.autosell_op = False
            
        

        # 손해 매도
        elif stop_price >= price:
            coin_balance = upbit.get_balance(coin_ticker) # 내가 산 코인 수량 
            upbit.sell_market_order(coin_ticker, coin_balance)
            
            self.in_list.delete(0,END)
            self.info_sell()
            
            self.autosell_op = False
        
        
        if self.autosell_op is True:
            self.after(2000, self.autoSell(sell_price, stop_price, coin_ticker))
        
        else:
                        
            notice = "현재-코인-주문-매수진행중-입니다."
            self.in_list.insert(END, notice)
            
            self.autobuy_op = True
            self.autoBuy()

                
                
        


            

                    
    
class Main_pump_add(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("DCTSS (Digital Currency Trading Support System)") # 타이틀
        self.resizable(False, False) # x(너비), y(높이) 값 변경 불가(창 크기 변경 불가)
        
        
        # 주문 프레임 (1-3)
        request_frame = LabelFrame(self, text="주문")
        request_frame.pack(padx=5, pady=5, ipady=5)

        # 1. 가상화폐 종류 옵션
        # 종류 레이블
        type_label = Label(request_frame, text="종류", width=8)
        type_label.pack(side="left", padx=1, pady=5)

        # 종류 콤보
        type_opt = []

        for i in upbit_krw_tickers: # krw-분리과정
            _, a = i.split("-")
            type_opt.append(a)

        cmb_type = ttk.Combobox(request_frame, state="readonly", values=type_opt, width=10)
        cmb_type.current(0)
        cmb_type.pack(side="left", padx=5, pady=5)
        cmb_type.bind("<<ComboboxSelected>>", self.Change_price_label)

        
        # 2. 현재가격 옵션   ,, 성능에 따라서 없어질 수 도 있음 현재가격갱신이 어려운경우
        # 현재가격 txt 레이블
        cur_price_txt_label = Label(request_frame, text="현재가격")
        cur_price_txt_label.pack(side="left", padx=5, pady=5)

        # 현재 가격 레이블
        cur_price_label = Label(request_frame, width=10, text="", anchor="e")
        cur_price_label.pack(side="left", padx=5, pady=5)

        # 현재가격 krw 레이블
        cur_price_krw_label = Label(request_frame, text="krw")
        cur_price_krw_label.pack(side="left")

        # 3. 주문수량 옵션
        # 주문수량 레이블
        amount_label = Label(request_frame, text="주문수량", width=8)
        amount_label.pack(side="left", padx=5, pady=5)

        # 주문수량 콤보
        amount_opt = ["5%" ,"10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        cmb_amount = ttk.Combobox(request_frame, state="readonly", values=amount_opt, width=10)
        cmb_amount.current(0)
        cmb_amount.pack(side="left", padx=5, pady=5)



        # 매수 프레임 (4)
        buy_frame = LabelFrame(self, text="매수")
        buy_frame.pack(padx=5, pady=5, ipady=5, fill="x")

        # 4. 매수가격 옵션
        # 매수가격 레이블
        buy_label = Label(buy_frame, text="매수가격", width=8)
        buy_label.pack(side="left", padx=5, pady=5)

        # 매수가격 krw 레이블
        buy_krw_label = Label(buy_frame, text="krw")
        buy_krw_label.pack(side="right")

        # 매수가격 엔트리
        buy_e = Entry(buy_frame, width=15) # 추가 될 예정
        buy_e.pack(side="right")

        # 매수가격 콤보
        buy_opt = ["직접입력" , "0%","1%", "2%", "3%", "4%" , "5%", "6%", "7%", "8%", "9%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        cmb_buy = ttk.Combobox(buy_frame, state="readonly", values=buy_opt, width=10)
        cmb_buy.current(0)
        cmb_buy.pack(side="right", padx=5, pady=5)
        cmb_buy.bind("<<ComboboxSelected>>", self.Change_price_buy)


        # 매도 프레임 (5)
        sell_frame = LabelFrame(self, text="매도")
        sell_frame.pack(padx=5, pady=5, ipady=5, fill="x")


        # 5. 매도가격 옵션
        # 매도가격 레이블
        sell_label = Label(sell_frame, text="매도가격", width=8)
        sell_label.pack(side="left", padx=5, pady=5)

        # 매도가격 krw 레이블
        sell_krw_label = Label(sell_frame, text="krw")
        sell_krw_label.pack(side="right")

        # 매도가격 엔트리
        sell_e = Entry(sell_frame, width=15) # 추가 될 예정
        sell_e.pack(side="right")

        # 매도가격 콤보
        sell_opt = ["직접입력" ,"0%","1%", "2%", "3%", "4%" ,"5%", "6%", "7%", "8%", "9%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        cmb_sell = ttk.Combobox(sell_frame, state="readonly", values=sell_opt, width=10)
        cmb_sell.current(0)
        cmb_sell.pack(side="right", padx=5, pady=5)
        cmb_sell.bind("<<ComboboxSelected>>",self.Change_price_sell)



        # 손절 프레임 (6)
        stoploss_frame = LabelFrame(self, text="손절")
        stoploss_frame.pack(padx=5, pady=5, ipady=5, fill="x")

        # 6. 손절가격 옵션
        # 손절가격 레이블
        stoploss_label = Label(stoploss_frame, text="매도가격", width=8)
        stoploss_label.pack(side="left", padx=5, pady=5)

        # 손절가격 krw 레이블
        stoploss_krw_label = Label(stoploss_frame, text="krw")
        stoploss_krw_label.pack(side="right")

        # 손절가격 엔트리
        stoploss_e = Entry(stoploss_frame, width=15) # 추가 될 예정
        stoploss_e.pack(side="right")

        # 손절가격 콤보
        stoploss_opt = ["직접입력" , "0%", "-1%", "-2%", "-3%", "-4%" ,"-5%", "-6%", "-7%", "-8%", "-9%", "-10%", "-20%", "-30%", "-40%", "-50%", "-60%", "-70%", "-80%", "-90%", "-100%"] # 추가 될 예정
        cmb_stoploss = ttk.Combobox(stoploss_frame, state="readonly", values=stoploss_opt, width=10)
        cmb_stoploss.current(0)
        cmb_stoploss.pack(side="right", padx=5, pady=5)
        cmb_stoploss.bind("<<ComboboxSelected>>",self.Change_price_stoploss)

        # 확인_취소 프레임
        okcnl_frame = Frame(self)
        okcnl_frame.pack(padx=5, pady=5, ipady=5, fill="x")

        # 7, 확인_취소 버튼
        btn_ok = Button(okcnl_frame, padx=5, pady=5, width=15, text="확인", command = self.Add_Confirm)
        btn_ok.pack(side="left")

        btn_cnl = Button(okcnl_frame, padx=5, pady=5, width=15, text="취소", command=self.quit)
        btn_cnl.pack(side="right")

        
        # 클래스 변수로 변경
        self.cur_price_label = cur_price_label
        self.cmb_amount = cmb_amount
        self.cmb_type = cmb_type
        self.cmb_buy = cmb_buy
        self.buy_e = buy_e
        self.cmb_sell = cmb_sell
        self.sell_e = sell_e
        self.cmb_stoploss = cmb_stoploss
        self.stoploss_e = stoploss_e


    # 콤보 선택시 함수
    def Change_price_label(self, *args):
        ticker = "KRW-" + self.cmb_type.get()
        self.cur_price_label['text'] = pyupbit.get_current_price(ticker)  # 코인종류를 변경할때마다 그때의 가격이 출력


        
        
    # 매수가격 함수
    def Change_price_buy(self, *args):
        if self.cmb_buy.get() == "직접입력":
            pass
        else:
            rate= self.cmb_buy.get()[:-1]
            cur_price= self.cur_price_label['text']
            self.buy_e.delete("0", END)
            self.buy_e.insert(0, Change(cur_price, rate))
            
    # 매도 가격 함수
    def Change_price_sell(self, *args):
         if self.cmb_sell.get() == "직접입력":
            pass
         else:
            rate= self.cmb_sell.get()[:-1]
            cur_price= self.buy_e.get()
            self.sell_e.delete("0", END)
            self.sell_e.insert(0, Change(cur_price, rate))
    
    # 손절 가격 함수
    def Change_price_stoploss(self, *args):
        if self.cmb_stoploss.get() == "직접입력":
            pass
        else:
            rate= self.cmb_stoploss.get()[:-1]
            cur_price= self.buy_e.get()
            self.stoploss_e.delete("0", END)
            self.stoploss_e.insert(0, Change(cur_price, rate))
     # 확인 버튼 함수
    def Add_Confirm(self):
        mm_txt = []
        mm_txt = [self.cmb_type.get(), self.cmb_amount.get(), self.buy_e.get(), self.sell_e.get(), self.stoploss_e.get()]
        self.master.standby_list.insert(END, mm_txt)

        
if __name__ == "__main__":
    Main_pump().mainloop()
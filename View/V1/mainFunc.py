# 리스트 삭제
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

            
            
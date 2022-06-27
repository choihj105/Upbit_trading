import tkinter as tk
import pyupbit
# 주문 리스트 프레임
class orderFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)

        # 리스트의 스크롤바
        self.in_scrollbar = tk.Scrollbar(self)
        self.in_scrollbar.pack(side="right", fill="y")

        # 리스트
        self.in_list = tk.Listbox(self, selectmode="extended", height=8, yscrollcommand=self.in_scrollbar.set)
        self.in_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.in_scrollbar.config(command=self.in_list.yview)

# 기능 프레임
class funcFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
    
        # 기능1 버튼
        self.btn1 = tk.Button(self, padx=5, pady=5, width=12, text= kwargs.get("n1"))
        self.btn1.pack(side="left")

        # 기능2 버튼
        self.btn2 = tk.Button(self, padx=5, pady=5, width=12, text= kwargs.get("n2"))
        self.btn2.pack(side="right")
         # command= self.Del_Cancle
          # command=self.mul_select
          # command = self.cnl_mul_select



# 현재 자산 프레임
class currencyFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        
        # krw 표시 레이블
        self.cur_asset_krw_label = tk.Label(self, text="krw")
        self.cur_asset_krw_label.pack(side="right")

        # 현재자산 레이블
        # cur_krw_balances = upbit.get_balance("KRW")
        self.cur_asset_label = tk.Label(self, width=15, anchor="e") # text=cur_krw_balances
        self.cur_asset_label.pack(side="right")

        # 주문가능 레이블
        self.cur_asset_txt_label = tk.Label(self, text="주문가능")
        self.cur_asset_txt_label.pack(side="right")



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
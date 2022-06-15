import tkinter as tk
import tkinter.ttk as ttk
import pyupbit

# 주문 프레임
class orderFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        
        # 1. 가상화폐 종류 옵션
        # 종류 레이블
        type_label = tk.Label(self, text="종류", width=8)
        type_label.pack(side="left", padx=1, pady=5)

        # 종류 콤보
        type_opt = []

        for i in pyupbit.get_tickers(fiat="KRW"): # krw-분리과정
            _, a = i.split("-")
            type_opt.append(a)

        self.cmb_type = ttk.Combobox(self, state="readonly", values=type_opt, width=10)
        self.cmb_type.current(0)
        self.cmb_type.pack(side="left", padx=5, pady=5)
        self.cmb_type.bind("<<ComboboxSelected>>", self.Change_price_label)

        # 2. 현재가격 옵션
        # 현재가격 txt 레이블
        cur_price_txt_label = tk.Label(self, text="현재가격")
        cur_price_txt_label.pack(side="left", padx=5, pady=5)

        # 현재 가격 레이블
        self.cur_price_label = tk.Label(self, width=10, text="", anchor="e")
        self.cur_price_label.pack(side="left", padx=5, pady=5)

        # 현재가격 krw 레이블
        cur_price_krw_label = tk.Label(self, text="krw")
        cur_price_krw_label.pack(side="left")

        # 3. 주문수량 옵션
        # 주문수량 레이블
        amount_label = tk.Label(self, text="주문수량", width=8)
        amount_label.pack(side="left", padx=5, pady=5)

        # 주문수량 콤보
        amount_opt = ["5%" ,"10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        self.cmb_amount = ttk.Combobox(self, state="readonly", values=amount_opt, width=10)
        self.cmb_amount.current(0)
        self.cmb_amount.pack(side="left", padx=5, pady=5)
    
    # 콤보 선택 시 가격 나오게 
    def Change_price_label(self, event):
        ticker = "KRW-" + self.cmb_type.get()
        self.cur_price_label['text'] = pyupbit.get_current_price(ticker)  # 코인종류를 변경할때마다 그때의 가격이 출력

# 가격 측정 프레임
class costFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)

        
        self.label = tk.Label(self, text= "가격", width=8)
        self.label.pack(side="left", padx=5, pady=5)

        # [매수, 매도, 손절] 가격 krw 레이블
        self.krw_label = tk.Label(self, text="krw")
        self.krw_label.pack(side="right")

        # [매수, 매도, 손절] 가격 엔트리
        self.e = tk.Entry(self, width=15) # 추가 될 예정
        self.e.pack(side="right")

        # [매수, 매도, 손절] 가격 콤보
        self.opt = ["직접입력" , "0%","1%", "2%", "3%", "4%" , "5%", "6%", "7%", "8%", "9%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        self.cmb = ttk.Combobox(self, state="readonly", values=self.opt, width=10)
        self.cmb.current(0)
        self.cmb.pack(side="right", padx=5, pady=5)
        self.cmb.bind("<<ComboboxSelected>>", self.Change_price_buy)

        
    # 매수 가격
    def Change_price_buy(self, *args):
        if self.cmb.get() == "직접입력":
            pass
        else:
            rate= self.cmb.get()[:-1]
            cur_price= self.cur_price_label['text']
            self.e.delete("0", tk.END)
            self.e.insert(0, Change(cur_price, rate))

    # 매도 가격 함수
    def Change_price_sell(self, *args):
         if self.cmb.get() == "직접입력":
            pass
         else:
            rate= self.cmb.get()[:-1]
            cur_price= self.e.get()
            self.e.delete("0", tk.END)
            self.e.insert(0, Change(cur_price, rate))
    
    # 손절 가격 함수
    def Change_price_stoploss(self, *args):
        if self.cmb.get() == "직접입력":
            pass
        else:
            rate= self.cmb.get()[:-1]
            cur_price= self.e.get()
            self.e.delete("0", tk.END)
            self.e.insert(0, Change(cur_price, rate))

'''
        # 4. 매수가격 옵션
        # 매수가격 레이블
        buy_label = tk.Label(self, text="매수가격", width=8)
        buy_label.pack(side="left", padx=5, pady=5)

        # 매수가격 krw 레이블
        buy_krw_label = tk.Label(self, text="krw")
        buy_krw_label.pack(side="right")

        # 매수가격 엔트리
        self.buy_e = tk.Entry(self, width=15) # 추가 될 예정
        self.buy_e.pack(side="right")

        # 매수가격 콤보
        buy_opt = ["직접입력" , "0%","1%", "2%", "3%", "4%" , "5%", "6%", "7%", "8%", "9%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        self.cmb_buy = ttk.Combobox(self, state="readonly", values=buy_opt, width=10)
        self.cmb_buy.current(0)
        self.cmb_buy.pack(side="right", padx=5, pady=5)
        self.cmb_buy.bind("<<ComboboxSelected>>", self.Change_price_buy)

    
        # 5. 매도가격 옵션
        # 매도가격 레이블
        sell_label = tk.Label(sell_frame, text="매도가격", width=8)
        sell_label.pack(side="left", padx=5, pady=5)

        # 매도가격 krw 레이블
        sell_krw_label = tk.Label(sell_frame, text="krw")
        sell_krw_label.pack(side="right")

        # 매도가격 엔트리
        self.sell_e = tk.Entry(sell_frame, width=15) # 추가 될 예정
        self.sell_e.pack(side="right")

        # 매도가격 콤보
        sell_opt = ["직접입력" ,"0%","1%", "2%", "3%", "4%" ,"5%", "6%", "7%", "8%", "9%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        self.cmb_sell = ttk.Combobox(sell_frame, state="readonly", values=sell_opt, width=10)
        self.cmb_sell.current(0)
        self.cmb_sell.pack(side="right", padx=5, pady=5)
        self.cmb_sell.bind("<<ComboboxSelected>>",self.Change_price_sell)

        # 6. 손절가격 옵션
        # 손절가격 레이블
        stoploss_label = tk.Label(stoploss_frame, text="매도가격", width=8)
        stoploss_label.pack(side="left", padx=5, pady=5)

        # 손절가격 krw 레이블
        stoploss_krw_label = tk.Label(stoploss_frame, text="krw")
        stoploss_krw_label.pack(side="right")

        # 손절가격 엔트리
        self.stoploss_e = tk.Entry(stoploss_frame, width=15) # 추가 될 예정
        self.stoploss_e.pack(side="right")

        # 손절가격 콤보
        stoploss_opt = ["직접입력" , "0%", "-1%", "-2%", "-3%", "-4%" ,"-5%", "-6%", "-7%", "-8%", "-9%", "-10%", "-20%", "-30%", "-40%", "-50%", "-60%", "-70%", "-80%", "-90%", "-100%"] # 추가 될 예정
        self.cmb_stoploss = ttk.Combobox(stoploss_frame, state="readonly", values=stoploss_opt, width=10)
        self.cmb_stoploss.current(0)
        self.cmb_stoploss.pack(side="right", padx=5, pady=5)
        self.cmb_stoploss.bind("<<ComboboxSelected>>",self.Change_price_stoploss)'''


# 기능 프레임
class funcFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
    
        # 기능1 버튼
        self.btn1 = tk.Button(self, padx=5, pady=5, width=15, text= kwargs.get("n1"))
        self.btn1.pack(side="left")

        # 기능2 버튼
        self.btn2 = tk.Button(self, padx=5, pady=5, width=15, text= kwargs.get("n2"))
        self.btn2.pack(side="right")
    
    # Add_Confirm

# 가격 조정 - 고쳐야 하는 함수!!
def Change(cur_price, rate):
    cur_price = float(cur_price)
    rate = float(rate)
    cur_price += (cur_price * (rate/100))
    
    # .. while 문으로 바꾸기..
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
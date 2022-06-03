import tkinter as tk
import tkinter.ttk as ttk
import pyupbit
from . import subMainFunc

class View_main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 주문 프레임 (1-3)
        request_frame = tk.LabelFrame(self, text="주문")
        request_frame.pack(padx=5, pady=5, ipady=5)

        # 1. 가상화폐 종류 옵션
        # 종류 레이블
        type_label = tk.Label(request_frame, text="종류", width=8)
        type_label.pack(side="left", padx=1, pady=5)

        # 종류 콤보
        type_opt = []

        for i in pyupbit.get_tickers(fiat="KRW"): # krw-분리과정
            _, a = i.split("-")
            type_opt.append(a)

        self.cmb_type = ttk.Combobox(request_frame, state="readonly", values=type_opt, width=10)
        self.cmb_type.current(0)
        self.cmb_type.pack(side="left", padx=5, pady=5)
        self.cmb_type.bind("<<ComboboxSelected>>", self.Change_price_label)

        
        # 2. 현재가격 옵션
        # 현재가격 txt 레이블
        cur_price_txt_label = tk.Label(request_frame, text="현재가격")
        cur_price_txt_label.pack(side="left", padx=5, pady=5)

        # 현재 가격 레이블
        self.cur_price_label = tk.Label(request_frame, width=10, text="", anchor="e")
        self.cur_price_label.pack(side="left", padx=5, pady=5)

        # 현재가격 krw 레이블
        cur_price_krw_label = tk.Label(request_frame, text="krw")
        cur_price_krw_label.pack(side="left")

        # 3. 주문수량 옵션
        # 주문수량 레이블
        amount_label = tk.Label(request_frame, text="주문수량", width=8)
        amount_label.pack(side="left", padx=5, pady=5)

        # 주문수량 콤보
        amount_opt = ["5%" ,"10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        self.cmb_amount = ttk.Combobox(request_frame, state="readonly", values=amount_opt, width=10)
        self.cmb_amount.current(0)
        self.cmb_amount.pack(side="left", padx=5, pady=5)



        # 매수 프레임 (4)
        buy_frame = tk.LabelFrame(self, text="매수")
        buy_frame.pack(padx=5, pady=5, ipady=5, fill="x")

        # 4. 매수가격 옵션
        # 매수가격 레이블
        buy_label = tk.Label(buy_frame, text="매수가격", width=8)
        buy_label.pack(side="left", padx=5, pady=5)

        # 매수가격 krw 레이블
        buy_krw_label = tk.Label(buy_frame, text="krw")
        buy_krw_label.pack(side="right")

        # 매수가격 엔트리
        self.buy_e = tk.Entry(buy_frame, width=15) # 추가 될 예정
        self.buy_e.pack(side="right")

        # 매수가격 콤보
        buy_opt = ["직접입력" , "0%","1%", "2%", "3%", "4%" , "5%", "6%", "7%", "8%", "9%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"] # 추가 될 예정
        self.cmb_buy = ttk.Combobox(buy_frame, state="readonly", values=buy_opt, width=10)
        self.cmb_buy.current(0)
        self.cmb_buy.pack(side="right", padx=5, pady=5)
        self.cmb_buy.bind("<<ComboboxSelected>>", self.Change_price_buy)


        # 매도 프레임 (5)
        sell_frame = tk.LabelFrame(self, text="매도")
        sell_frame.pack(padx=5, pady=5, ipady=5, fill="x")


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


        # 손절 프레임 (6)
        stoploss_frame = tk.LabelFrame(self, text="손절")
        stoploss_frame.pack(padx=5, pady=5, ipady=5, fill="x")

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
        self.cmb_stoploss.bind("<<ComboboxSelected>>",self.Change_price_stoploss)

        # 확인_취소 프레임
        okcnl_frame = tk.Frame(self)
        okcnl_frame.pack(padx=5, pady=5, ipady=5, fill="x")

        # 7, 확인_취소 버튼
        self.btn_ok = tk.Button(okcnl_frame, padx=5, pady=5, width=15, text="확인")
        self.btn_ok.pack(side="left")
        # Add_Confirm

        self.btn_cnl = tk.Button(okcnl_frame, padx=5, pady=5, width=15, text="취소", command=quit)
        self.btn_cnl.pack(side="right")
        
    # 콤보 선택 시 가격 나오게
    def Change_price_label(self, event):
        ticker = "KRW-" + self.cmb_type.get()
        self.cur_price_label['text'] = pyupbit.get_current_price(ticker)  # 코인종류를 변경할때마다 그때의 가격이 출력

    # 매수 가격
    def Change_price_buy(self, *args):
        if self.cmb_buy.get() == "직접입력":
            pass
        else:
            rate= self.cmb_buy.get()[:-1]
            cur_price= self.cur_price_label['text']
            self.buy_e.delete("0", tk.END)
            self.buy_e.insert(0, subMainFunc.Change(cur_price, rate))

    # 매도 가격 함수
    def Change_price_sell(self, *args):
         if self.cmb_sell.get() == "직접입력":
            pass
         else:
            rate= self.cmb_sell.get()[:-1]
            cur_price= self.buy_e.get()
            self.sell_e.delete("0", tk.END)
            self.sell_e.insert(0, subMainFunc.Change(cur_price, rate))
    
    # 손절 가격 함수
    def Change_price_stoploss(self, *args):
        if self.cmb_stoploss.get() == "직접입력":
            pass
        else:
            rate= self.cmb_stoploss.get()[:-1]
            cur_price= self.buy_e.get()
            self.stoploss_e.delete("0", tk.END)
            self.stoploss_e.insert(0, subMainFunc.Change(cur_price, rate))

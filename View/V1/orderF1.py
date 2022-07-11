import tkinter as tk
import tkinter.messagebox as msgbox
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

        # 캔버스 도형 : 주문 체크용
        self.in_switch = tk.Canvas(self, width= 10, height=20, bg="#FF6666")
        self.in_switch.pack(side="left",fill="y", pady=5, anchor="w")


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

class my_Msg():
    def info_start():
        msgbox.showinfo("알림", "정상적으로 주문이 접수 되었습니다.")
    def info_error():
        msgbox.showerror("에러", "주문 오류가 발생하였습니다. 주문을 해주세요.")
    def info_error2():
        msgbox.showerror("에러", "주문 오류가 발생하였습니다. 빈값을 확인해주세요")
    def info_error3():
        msgbox.showinfo("알림", "잔액이 부족합니다.")
    def info_error4():
        msgbox.showerror("에러", "취소 오류가 발생하였습니다.")
    def info_buy():
        msgbox.showinfo("알림", "정상적으로 매수 완료되었습니다.")
    def info_sell():
        msgbox.showinfo("알림", "정상적으로 매도 완료되었습니다.")
    def info_cnl():
        msgbox.showinfo("알림", "정상적으로 주문이 취소되었습니다.")
    def info_auto():
        msgbox.showinfo("알림", "정상적으로 자동매매주문이 접수되었습니다.")
    
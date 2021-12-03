import tkinter as tk
from tkinter.constants import BOTH, TOP

class View_main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # 진행중인 주문 리스트 프레임
        in_list_frame = tk.LabelFrame(self, text="진행중인 주문")
        in_list_frame.pack(fill="both", padx=5, pady=5, ipady=5)

        # 매매진행중인 리스트의 스크롤바
        in_scrollbar = tk.Scrollbar(in_list_frame)
        in_scrollbar.pack(side="right", fill="y")

        # 매매진행중인 리스트
        self.in_list = tk.Listbox(in_list_frame, selectmode="extended", height=8, yscrollcommand=in_scrollbar.set)
        self.in_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        in_scrollbar.config(command=self.in_list.yview)


        # 매매대기중인 리스트 프레임
        standby_list_frame = tk.LabelFrame(self, text="대기중인 주문")
        standby_list_frame.pack(fill="both", padx=5, pady=5, ipady=5)

        # 매매대기중인 리스트의 스크롤바
        standby_scrollbar = tk.Scrollbar(standby_list_frame)
        standby_scrollbar.pack(side="right", fill="y")

        # 매매대기중인 리스트
        self.standby_list = tk.Listbox(standby_list_frame, selectmode="extended", height=8, yscrollcommand=standby_scrollbar.set)
        self.standby_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)


        # 기능 프레임 (추가, 삭제버튼 )
        func_frame = tk.Frame(self)
        func_frame.pack(fill="both", padx=5, pady=5)

        # 추가버튼
        btn_add_func = tk.Button(func_frame, padx=5, pady=5, width=12, text="추가") # command= Main_pump_add
        btn_add_func.pack(side="left")

        # 삭제버튼
        btn_del_func = tk.Button(func_frame, padx=5, pady=5, width=12, text="삭제") # command= self.Del_Cancle
        btn_del_func.pack(side="right")
        
        
        # 기능 프레임2 (실행, 실행취소버튼 )
        func_frame2 = tk.Frame(self)
        func_frame2.pack(fill="both", padx=5, pady=5)

        # 실행버튼
        
        btn_exec_func = tk.Button(func_frame2, padx=5, pady=5, width=12, text="실행" ) # command=self.mul_select
        btn_exec_func.pack(side="left")

        # 실행취소버튼
        btn_exec_cnl_func = tk.Button(func_frame2, padx=5, pady=5, width=12, text="실행취소") # command = self.cnl_mul_select
        btn_exec_cnl_func.pack(side="right")
        
        
        # 기능 프레임3 (자동매수, 자동매수취소버튼 )
        func_frame3 = tk.Frame(self)
        func_frame3.pack(fill="both", padx=5, pady=5)

        # 자동매수버튼
        
        btn_auto_func = tk.Button(func_frame3, padx=5, pady=5, width=12, text="자동매수") # command=self.autoBuy
        btn_auto_func.pack(side="left")

        # 자동매수취소버튼
        btn_auto_cnl_func = tk.Button(func_frame3, padx=5, pady=5, width=12, text="자동매수취소")
        btn_auto_cnl_func.pack(side="right")
        
        
        
        # 주문가능한 현재자산 프레임
        cur_asset_frame = tk.Frame(self)
        cur_asset_frame.pack(fill="both", padx=5, pady=5, ipady=10, ipadx=10)

        # krw 표시 레이블
        cur_asset_krw_label = tk.Label(cur_asset_frame, text="krw")
        cur_asset_krw_label.pack(side="right")

        # 현재자산 레이블
        # cur_krw_balances = upbit.get_balance("KRW")
        cur_asset_label = tk.Label(cur_asset_frame, width=15, anchor="e") # text=cur_krw_balances
        cur_asset_label.pack(side="right")

        # 주문가능 레이블
        cur_asset_txt_label = tk.Label(cur_asset_frame, text="주문가능")
        cur_asset_txt_label.pack(side="right")
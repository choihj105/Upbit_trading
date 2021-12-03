import tkinter as tk

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
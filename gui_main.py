import datetime, json, os, tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from crawler import get_hknu_meal, get_hknu_weather

class Team2_Bot:
    def __init__(self):
        self.file = "timetable.json"
        self.locations = {
            "공학관": "제1공학관은 정문 근처, 제2공학관은 본관 뒤편입니다. 제3공학관은 쪽문쪽 거대한 건물입니다.",
            "인문사회관": "운동장 근처에 있는 건물입니다.",
            "학생회관": "2층에 학생식당이 있습니다.",
            "대학본부": "학교 중앙에 위치한 건물입니다.",
            "학생성공관": "대학본부 뒤편에 위치한 건물입니다.",
            "농학관": "제2농학관은 학교 정문 바로 우측건물, 제 1농학관은 학생회관 근처에 위치하고 있습니다.",
            "기계공학관": "기계공학관은 학교 후문에 위치하고 있습니다.",
            "공동실험실습관": "공동실험실습관은 제3공학관 근처에 위치하고 있습니다." 
        }
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return {d: "" for d in list("월화수목금")}

    def save_all_data(self, new_data):
        self.data.update(new_data)
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def respond(self, msg):
        # [추가] 시각적 시간표 출력 신호 감지
        if any(x in msg for x in ["보여줘", "보여줄래", "찐 시간표", "내 시간표"]):
            return "SIGNAL_SHOW_VISUAL"

        target_day = None
        for d in list("월화수목금토일"):
            if d in msg:
                target_day = d
                break
        
        today_idx = datetime.datetime.now().weekday()
        today_day = "월화수목금토일"[today_idx]

        if any(x in msg for x in ["학식", "밥", "메뉴", "점심", "식단"]):
            if target_day and target_day != today_day:
                return f"식단은 '오늘' 메뉴만 실시간 조회가 가능합니다. 대신 오늘 식단을 보여드릴게요:\n\n{get_hknu_meal()}"
            return f"🍴 오늘의 식단입니다:\n\n{get_hknu_meal()}"
        
        if "날씨" in msg:
            return get_hknu_weather()
        
        if any(x in msg for x in ["시간표", "수업", "강의"]):
            query_day = target_day if target_day else today_day
            schedule = self.data.get(query_day, "").strip()
            if not schedule:
                return f"📅 {query_day}요일은 등록된 일정이 없습니다. 하단 버튼을 눌러 등록해주세요!"
            return f"📅 {query_day}요일 등록된 일정입니다:\n{schedule}"
        
        if any(x in msg for x in ["위치", "어디", "장소"]):
            for k, v in self.locations.items():
                if k in msg: return f"📍 {k} 위치: {v}"
            return "정확한 건물명을 입력해주세요. (예: 공학관 어디야?)"
            
        return "죄송해요, 잘 이해하지 못했어요. '식단', '날씨', '월요일 수업' 처럼 질문해 보세요!"

class ChatGUI:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root
        root.title("한경국립대 나만의 학사비서"); root.geometry("450x650"); root.configure(bg="#2C3E50")
        
        self.log = scrolledtext.ScrolledText(root, width=50, height=28, bg="#ECF0F1", font=("맑은 고딕", 10), state='disabled')
        self.log.pack(pady=10)

        f = tk.Frame(root, bg="#2C3E50"); f.pack(fill="x", padx=10)
        self.ent = tk.Entry(f, width=32, font=("맑은 고딕", 11)); self.ent.pack(side="left", padx=5, pady=5)
        self.ent.bind("<Return>", self.send)
        
        tk.Button(f, text="전송", command=self.send, bg="#3498DB", fg="white", width=8).pack(side="left")
        tk.Button(root, text="📅 내 주간 시간표 한꺼번에 관리하기", command=self.open_batch_form, bg="#E67E22", fg="white", font=("맑은 고딕", 10, "bold")).pack(fill="x", padx=15, pady=5)
        
        self.msg("시스템", "반갑습니다! 나만의 학사비서 챗봇입니다.\n'내 시간표 보여줘'라고 입력하면 이미지 형태의 시간표를 볼 수 있어요!")

    def send(self, e=None):
        txt = self.ent.get().strip()
        if txt:
            self.msg("나", txt); self.ent.delete(0, "end")
            response = self.bot.respond(txt)
            
            # 시각적 시간표 신호일 경우 함수 실행
            if response == "SIGNAL_SHOW_VISUAL":
                self.msg("챗봇", "요청하신 찐 시간표 이미지를 생성했습니다! 짜잔~ ✨")
                self.show_visual_timetable()
            else:
                self.msg("챗봇", response)

    def msg(self, sender, m):
        self.log.config(state='normal'); self.log.insert("end", f"[{sender}]: {m}\n\n")
        self.log.config(state='disabled'); self.log.yview("end")

    # [추가] 찐 시간표 이미지 형태의 팝업창
    def show_visual_timetable(self):
        win = tk.Toplevel(self.root)
        win.title("나의 찐 시간표")
        win.geometry("650x450")
        win.configure(bg="#FDF6E3") # 레트로한 미색 배경

        tk.Label(win, text="시 간 표", font=("궁서", 35, "bold"), bg="#FDF6E3", fg="#333").pack(pady=20)

        # 격자 프레임
        table_frame = tk.Frame(win, bg="black", bd=2)
        table_frame.pack(padx=30, pady=10, fill="both", expand=True)

        days = list("월화수목금")
        
        # 헤더 레이아웃
        for i, day in enumerate(days):
            lbl = tk.Label(table_frame, text=day, font=("맑은 고딕", 13, "bold"), 
                           bg="#D7D7D7", fg="black", borderwidth=1, relief="solid", width=12, height=2)
            lbl.grid(row=0, column=i, sticky="nsew")

        # 데이터 레이아웃
        for i, day in enumerate(days):
            content = self.bot.data.get(day, "")
            # 가독성을 위해 슬래시나 공백을 줄바꿈으로 변경
            display_text = content.replace("/", "\n").replace(" ", "\n")
            
            lbl = tk.Label(table_frame, text=display_text, font=("맑은 고딕", 11), 
                           bg="white", fg="black", borderwidth=1, relief="solid", 
                           width=12, height=10, justify="center")
            lbl.grid(row=1, column=i, sticky="nsew")

        # 셀 간격 자동 조정
        for i in range(5):
            table_frame.grid_columnconfigure(i, weight=1)

    def open_batch_form(self):
        win = tk.Toplevel(self.root); win.title("주간 시간표 일괄 관리"); win.geometry("380x480")
        win.configure(bg="#F3F4F6")

        tk.Label(win, text="[ 월~금 시간표 수정 ]", font=("맑은 고딕", 12, "bold"), bg="#F3F4F6").pack(pady=15)
        
        entry_widgets = {}
        for day in list("월화수목금"):
            row = tk.Frame(win, bg="#F3F4F6")
            row.pack(fill="x", padx=20, pady=5)
            tk.Label(row, text=f"{day}요일", width=6, anchor="w", bg="#F3F4F6", font=("맑은 고딕", 10)).pack(side="left")
            ent = tk.Entry(row, font=("맑은 고딕", 10))
            ent.pack(side="left", fill="x", expand=True, padx=5)
            ent.insert(0, self.bot.data.get(day, ""))
            entry_widgets[day] = ent

        def save_all():
            new_data = {day: widget.get() for day, widget in entry_widgets.items()}
            self.bot.save_all_data(new_data)
            messagebox.showinfo("저장 완료", "주간 시간표가 모두 저장되었습니다!")
            self.msg("시스템", "전체 시간표가 업데이트 되었습니다.")
            win.destroy()

        # 저장 버튼과 이미지 보기 버튼 배치
        tk.Button(win, text="전체 저장하기", command=save_all, bg="#27AE60", fg="white", font=("맑은 고딕", 10, "bold"), height=2).pack(fill="x", padx=50, pady=15)
        tk.Button(win, text="📊 현재 시간표 이미지로 보기", command=self.show_visual_timetable, bg="#3498DB", fg="white", font=("맑은 고딕", 10)).pack(fill="x", padx=50, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    ChatGUI(root, Team2_Bot())
    root.mainloop()
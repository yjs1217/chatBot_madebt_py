import datetime
import tkinter as tk
from tkinter import scrolledtext

class Team2_GUI_Chatbot:
    def __init__(self):
        self.bot_name = "2팀 학사 안내 시스템"
        
        # 데이터 정의 (기존 데이터 유지)
        self.timetable = {
            "월": "10:00 파이썬 기초 / 14:00 데이터 사이언스",
            "화": "11:00 객체지향 프로그래밍 / 15:00 운영체제",
            "수": "10:00 네트워크 보안 / 13:00 팀 프로젝트 실습",
            "목": "09:00 인공지능 / 14:00 데이터베이스",
            "금": "11:00 웹 프로그래밍 / 16:00 영어 회화"
        }
        
        self.locations = {
            "공학관": "정문 우측 3층 건물입니다.",
            "인문관": "학생회관 옆 흰색 건물입니다.",
            "학생회관": "매점과 동아리방이 있는 건물입니다."
        }

    # 로직 함수들 (기존과 동일)
    def get_meal_info(self):
        return "오늘의 학식(중식): 돈까스, 제육볶음, 미역국입니다.[cite: 1]"

    def get_today_schedule(self):
        now = datetime.datetime.now()
        days = ["월", "화", "수", "목", "금", "토", "일"]
        today_day = days[now.weekday()]
        schedule = self.timetable.get(today_day, "오늘은 수업이 없습니다.")
        return f"오늘({today_day}요일) 수업 일정입니다: {schedule}[cite: 1]"

    def get_location(self, query):
        for building, desc in self.locations.items():
            if building in query:
                return f"{building} 위치: {desc}[cite: 1]"
        return "해당 건물의 위치 정보를 찾을 수 없습니다.[cite: 1]"

    def get_weather(self):
        return "현재 학교 주변 기온은 18도, 구름 조금입니다.[cite: 1]"

    # 답변 엔진[cite: 1]
    def response_engine(self, user_msg):
        user_msg = user_msg.strip()
        if "안녕" in user_msg or "시작" in user_msg:
            return f"반갑습니다! {self.bot_name}입니다. 무엇을 도와드릴까요?[cite: 1]"
        elif "학식" in user_msg or "밥" in user_msg:
            return self.get_meal_info()
        elif "시간표" in user_msg or "수업" in user_msg:
            return self.get_today_schedule()
        elif "위치" in user_msg or "어디" in user_msg:
            return self.get_location(user_msg)
        elif "날씨" in user_msg:
            return self.get_weather()
        else:
            return "궁금한 키워드(학식, 시간표, 위치, 날씨)를 입력해주세요.[cite: 1]"

# --- GUI 클래스 정의 ---
class ChatGUI:
    def __init__(self, master, chatbot):
        self.master = master
        self.chatbot = chatbot
        master.title("2팀 학사 안내 챗봇 서비스")
        master.geometry("400x550")
        master.configure(bg="#A9BDCE") # 메신저 배경색

        # 채팅 로그 출력창
        self.chat_log = scrolledtext.ScrolledText(master, width=45, height=25, bg="white", state='disabled')
        self.chat_log.pack(padx=10, pady=10)

        # 입력창
        self.input_field = tk.Entry(master, width=35)
        self.input_field.pack(side=tk.LEFT, padx=10, pady=10)
        self.input_field.bind("<Return>", self.send_message) # 엔터키 연결

        # 전송 버튼
        self.send_button = tk.Button(master, text="전송", command=self.send_message, bg="#FEE500")
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.display_message("시스템", f"{self.chatbot.bot_name}에 오신 것을 환영합니다![cite: 1]")

    def send_message(self, event=None):
        user_text = self.input_field.get()
        if not user_text.strip(): return

        self.display_message("나", user_text)
        self.input_field.delete(0, tk.END)

        # 챗봇 답변 가져오기
        response = self.chatbot.response_engine(user_text)
        self.display_message("챗봇", response)

    def display_message(self, sender, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, f"[{sender}]: {message}\n\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    bot = Team2_GUI_Chatbot()
    gui = ChatGUI(root, bot)
    root.mainloop()
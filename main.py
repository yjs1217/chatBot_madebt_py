import datetime

class Team2_FinalChatbot:
    def __init__(self):
        self.bot_name = "2팀 학사 안내 시스템" #
        
        # [데이터 정의] 계획서에 명시된 정보들
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

    # 기능 1: 식단 안내 (크롤링 토대)
    def get_meal_info(self):
        # 3일 완성 목표 시, 여기에 크롤링 코드를 추가하세요.
        # 현재는 계획서 기반 고정 텍스트입니다.
        return "오늘의 학식(중식): 돈까스, 제육볶음, 미역국입니다.[cite: 1]"

    # 기능 2: 시간표 안내[cite: 1]
    def get_today_schedule(self):
        now = datetime.datetime.now()
        days = ["월", "화", "수", "목", "금", "토", "일"]
        today_day = days[now.weekday()]
        
        schedule = self.timetable.get(today_day, "오늘은 수업이 없습니다.")
        return f"오늘({today_day}요일) 수업 일정입니다: {schedule}"

    # 기능 3: 강의실 및 위치 안내[cite: 1]
    def get_location(self, query):
        for building, desc in self.locations.items():
            if building in query:
                return f"{building} 위치: {desc}"
        return "해당 건물의 위치 정보를 데이터베이스에서 찾을 수 없습니다."

    # 기능 4: 날씨 정보[cite: 1]
    def get_weather(self):
        # API 연결 전 임시 메시지
        return "현재 학교 주변 기온은 18도, 구름 조금입니다."

    # [핵심] 모든 기능을 제어하는 컨트롤러
    def response_engine(self, user_msg):
        user_msg = user_msg.strip()

        if "안녕" in user_msg or "시작" in user_msg:
            return f"반갑습니다! {self.bot_name}입니다. '식단', '시간표', '위치', '날씨' 중 궁금한 것을 물어보세요!"

        elif "학식" in user_msg or "밥" in user_msg or "메뉴" in user_msg:
            return self.get_meal_info()

        elif "시간표" in user_msg or "수업" in user_msg:
            return self.get_today_schedule()

        elif "위치" in user_msg or "어디" in user_msg or "동" in user_msg:
            return self.get_location(user_msg)

        elif "날씨" in user_msg:
            return self.get_weather()

        elif "종료" in user_msg or "끝" in user_msg:
            return "EXIT_SIGNAL"

        else:
            return "이해하지 못했습니다. 다시 말씀해 주시겠어요?"

# --- 실행부 (CLI 인터페이스) ---
def start_project():
    chatbot = Team2_FinalChatbot()
    print(f"--- {chatbot.bot_name} 작동 시작 (계획서 기능 통합) ---")
    
    while True:
        user_input = input("\n[사용자 질문]: ")
        
        reply = chatbot.response_engine(user_input)
        
        if reply == "EXIT_SIGNAL":
            print("챗봇을 종료합니다. 프로젝트 성공을 빕니다!")
            break
            
        print(f"[AI 답변]: {reply}")

if __name__ == "__main__":
    start_project()

    #이 기반 위에 실시간 크롤링이나 API 연동만 추가하면 완벽한 결과물이 됩니다.
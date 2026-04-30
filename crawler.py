import requests
from bs4 import BeautifulSoup
import datetime
import urllib3

# 보안 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HKNU_API:
    def __init__(self):
        self.url = "https://www.hknu.ac.kr/kor/670/subview.do"
        # 브라우저처럼 보이게 만드는 '가짜 명함' (매우 중요)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.hknu.ac.kr/',
            'Connection': 'keep-alive'
        }

    def fetch_meal_data(self):
        """학교 홈페이지에서 데이터를 강제로 호출하여 가져옵니다."""
        try:
            # 1. 세션 생성 (쿠키 등을 자동으로 관리)
            session = requests.Session()
            response = session.get(self.url, headers=self.headers, verify=False, timeout=15)
            
            if response.status_code != 200:
                return f"서버 응답 오류 (코드: {response.status_code})"

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. 식단 테이블 찾기
            table = soup.find('table', {'class': 'table_st'})
            if not table:
                return "식단 데이터를 찾을 수 없습니다. (사이트 점검 중)"

            # 3. 요일 판단 (오늘의 인덱스)
            day_idx = datetime.datetime.now().weekday() # 월:0, 화:1, 수:2, 목:3, 금:4
            if day_idx > 4:
                return "오늘은 주말입니다. 학생식당은 운영하지 않습니다."

            # 4. 데이터 파싱 (한경대 표 구조 분석)
            # tr[0]이 점심(중식) 메뉴 행입니다.
            rows = table.find('tbody').find_all('tr')
            if not rows:
                return "등록된 식단 행이 없습니다."

            # 한경대 구조: 0번 칸은 '중식', 1번 칸부터 월요일 시작
            cells = rows[0].find_all('td')
            
            # 오늘 날짜에 맞는 칸 선택 (day_idx + 1)
            target_cell = cells[day_idx + 1]
            
            # HTML 태그 제거 및 가독성 좋게 줄바꿈 처리
            menu_text = target_cell.get_text(separator="\n").strip()
            
            if len(menu_text) < 5 or "등록된" in menu_text:
                return f"오늘({['월','화','수','목','금'][day_idx]})은 등록된 식단이 없습니다."

            return menu_text

        except Exception as e:
            return f"데이터 호출 중 치명적 오류: {str(e)}"

# 챗봇에서 사용할 수 있도록 외부 함수로 노출
def get_hknu_meal():
    api = HKNU_API()
    return api.fetch_meal_data()

def get_hknu_weather():
    """날씨 정보 API (네이버 검색 결과 활용)"""
    try:
        url = "https://search.naver.com/search.naver?query=안성+날씨"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        temp = soup.select_one(".temperature_text > strong").text.replace("현재 온도", "")
        desc = soup.select_one(".before_slash").text
        return f"현재 안성(학교) 날씨는 {desc} ({temp})입니다."
    except:
        return "날씨 정보를 가져올 수 없습니다."
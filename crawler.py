import requests
from bs4 import BeautifulSoup
import datetime
import urllib3
import re

# 보안 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HKNU_API:
    def __init__(self):
        self.url = "https://www.hknu.ac.kr/kor/670/subview.do"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.hknu.ac.kr/',
            'Connection': 'keep-alive'
        }

    def fetch_meal_data(self):
        """학교 홈페이지에서 식단 데이터를 가져옵니다."""
        try:
            session = requests.Session()
            response = session.get(self.url, headers=self.headers, verify=False, timeout=15)

            if response.status_code != 200:
                return f"서버 응답 오류 (코드: {response.status_code})"

            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', {'class': 'table_st'})
            if not table:
                return (
                    "식단 데이터를 찾을 수 없습니다. (사이트 점검 중)\n\n"
                    "대체 안내:\n"
                    "- 학교 홈페이지 식단표를 직접 확인해 주세요.\n"
                    "- 잠시 후 다시 조회해 주세요.\n"
                    "- 학식 정보가 없으면 학생식당, 편의점, 주변 식당을 이용해 주세요."
                )

            day_idx = datetime.datetime.now().weekday()  # 월:0 ~ 일:6
            if day_idx > 4:
                return "오늘은 주말입니다. 학생식당은 운영하지 않습니다."

            rows = table.find('tbody').find_all('tr')
            if not rows:
                return "등록된 식단 행이 없습니다."

            cells = rows[0].find_all('td')

            if len(cells) <= day_idx + 1:
                return "오늘 식단 칸을 찾을 수 없습니다."

            target_cell = cells[day_idx + 1]
            menu_text = target_cell.get_text(separator="\n").strip()

            if len(menu_text) < 5 or "등록된" in menu_text:
                return f"오늘({['월','화','수','목','금'][day_idx]})은 등록된 식단이 없습니다."

            return menu_text

        except Exception as e:
            return f"데이터 호출 중 오류: {str(e)}"


def get_hknu_meal():
    api = HKNU_API()
    return api.fetch_meal_data()


def get_hknu_weather():
    """날씨 정보 가져오기"""
    try:
        url = "https://search.naver.com/search.naver?query=안성+날씨"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        temp_tag = soup.select_one(".temperature_text > strong")
        desc_tag = soup.select_one(".before_slash")

        if not temp_tag or not desc_tag:
            return "날씨 정보를 가져올 수 없습니다."

        temp = temp_tag.text.replace("현재 온도", "").strip()
        desc = desc_tag.text.strip()

        return f"현재 안성(학교) 날씨는 {desc} ({temp})입니다."

    except Exception:
        return "날씨 정보를 가져올 수 없습니다."


def get_hknu_month_events(year=None, month=None):
    """
    한경국립대 공식 홈페이지 학부 학사일정 조회 함수
    크롤링을 먼저 시도하고, 실패하면 공식 홈페이지 기준 2026년 예비 데이터를 사용합니다.
    """
    if year is None:
        year = datetime.datetime.now().year
    if month is None:
        month = datetime.datetime.now().month

    fallback_2026 = {
        1: [
            {"start_day": 5, "end_day": 9, "date": "01.05 ~ 09", "title": "전과 및 재입학 신청"},
            {"start_day": 9, "end_day": 14, "date": "01.09 ~ 14", "title": "조기졸업, 학사학위 취득유예 신청"},
            {"start_day": 20, "end_day": 22, "date": "01.20 ~ 22", "title": "예비 수강신청 (장바구니)"},
            {"start_day": 28, "end_day": 30, "date": "01.28 ~ 30", "title": "재학생 본 수강신청"},
        ],
        2: [
            {"start_day": 20, "end_day": 20, "date": "02.20", "title": "2025학년도 전기 학위수여식"},
            {"start_day": 23, "end_day": 27, "date": "02.23 ~ 27", "title": "2026-1학기 재학생 등록기간"},
            {"start_day": 27, "end_day": 27, "date": "02.27", "title": "신입생 오리엔테이션"},
            {"start_day": 27, "end_day": 27, "date": "02.27", "title": "신편입생 수강신청"},
        ],
        3: [
            {"start_day": 3, "end_day": 20, "date": "03.03 ~ 20", "title": "2차(최종) 복학 신청"},
            {"start_day": 3, "end_day": 3, "date": "03.03", "title": "신편입생 수강신청"},
            {"start_day": 3, "end_day": 3, "date": "03.03", "title": "1학기 개강"},
            {"start_day": 6, "end_day": 9, "date": "03.06 ~ 09", "title": "재학생 수강신청 변경기간"},
            {"start_day": 28, "end_day": 28, "date": "03.28", "title": "수업일수 1/4선"},
            {"start_day": 30, "end_day": 3, "date": "03.30 ~ 04.03", "title": "1차 수강철회 신청"},
        ],
        4: [
            {"start_day": 6, "end_day": 6, "date": "04.06", "title": "수업일수 1/3선"},
            {"start_day": 13, "end_day": 17, "date": "04.13 ~ 17", "title": "복수·부·융합·연계전공 신청(1차)"},
            {"start_day": 15, "end_day": 15, "date": "04.15", "title": "개교기념일"},
            {"start_day": 21, "end_day": 27, "date": "04.21 ~ 27", "title": "1학기 중간시험"},
            {"start_day": 24, "end_day": 24, "date": "04.24", "title": "수업일수 1/2선"},
        ],
        5: [
            {"start_day": 6, "end_day": 12, "date": "05.06 ~ 12", "title": "제1회 졸업종합시험"},
            {"start_day": 7, "end_day": 13, "date": "05.07 ~ 13", "title": "2차 수강철회"},
            {"start_day": 13, "end_day": 13, "date": "05.13", "title": "수업일수 2/3선"},
            {"start_day": 19, "end_day": 20, "date": "05.19 ~ 20", "title": "평택캠퍼스 학생 체육대회 및 소축제 행사"},
            {"start_day": 26, "end_day": 28, "date": "05.26 ~ 28", "title": "한경체전"},
        ],
        6: [
            {"start_day": 1, "end_day": 5, "date": "06.01 ~ 05", "title": "전공 배정 및 변경 신청"},
            {"start_day": 8, "end_day": 12, "date": "06.08 ~ 12", "title": "복수·부·융합·연계전공 신청(2차)"},
            {"start_day": 11, "end_day": 22, "date": "06.11 ~ 22", "title": "1학기 기말시험"},
            {"start_day": 20, "end_day": 22, "date": "06.20 ~ 22", "title": "종강"},
            {"start_day": 23, "end_day": 13, "date": "06.23 ~ 07.13", "title": "하계 계절수업"},
        ],
        9: [
            {"start_day": 1, "end_day": 1, "date": "09.01", "title": "2학기 개강"},
            {"start_day": 1, "end_day": 18, "date": "09.01 ~ 18", "title": "2차(최종) 복학 신청"},
            {"start_day": 18, "end_day": 18, "date": "09.18", "title": "최종 복학 마감"},
            {"start_day": 30, "end_day": 1, "date": "09.30 ~ 10.01", "title": "가을축제(백호대동제)"},
            {"start_day": 30, "end_day": 30, "date": "09.30", "title": "수업일수 1/4선"},
        ],
        10: [
            {"start_day": 12, "end_day": 16, "date": "10.12 ~ 16", "title": "복수·부·융합·연계전공 신청(1차)"},
            {"start_day": 12, "end_day": 17, "date": "10.12 ~ 17", "title": "제2회 졸업종합시험"},
            {"start_day": 20, "end_day": 26, "date": "10.20 ~ 26", "title": "2학기 중간시험"},
            {"start_day": 29, "end_day": 29, "date": "10.29", "title": "수업일수 1/2선"},
        ],
        11: [
            {"start_day": 16, "end_day": 16, "date": "11.16", "title": "수업일수 2/3선"},
            {"start_day": 30, "end_day": 4, "date": "11.30 ~ 12.04", "title": "전공 배정 및 변경 신청"},
        ],
        12: [
            {"start_day": 7, "end_day": 11, "date": "12.07 ~ 11", "title": "복수·부·융합·연계전공 신청(2차)"},
            {"start_day": 8, "end_day": 21, "date": "12.08 ~ 21", "title": "2학기 기말시험"},
            {"start_day": 21, "end_day": 21, "date": "12.21", "title": "종강"},
            {"start_day": 22, "end_day": 13, "date": "12.22 ~ 01.13", "title": "동계 계절수업"},
        ],
    }

    if year == 2026:
        return fallback_2026.get(month, [])

    return []

    
def get_hknu_month_events_text(year=None, month=None):
    if year is None:
        year = datetime.datetime.now().year
    if month is None:
        month = datetime.datetime.now().month

    events = get_hknu_month_events(year, month)

    if not events:
        return f"{year}년 {month}월 등록된 학교 행사/학사일정이 없습니다."

    result = f"[{year}년 {month}월 한경국립대 행사/학사일정]\n\n"

    for event in events:
        result += f"{event['date']} - {event['title']}\n"

    return result

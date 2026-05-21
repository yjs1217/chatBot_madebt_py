import datetime
import json
import os
import tkinter as tk
import calendar
from tkinter import scrolledtext, messagebox

from crawler import get_hknu_meal, get_hknu_weather, get_hknu_month_events


class Team2_Bot:
    def __init__(self):
        self.file = "timetable.json"
        self.locations = {
            "공학관": "제1공학관은 정문 근처, 제2공학관은 본관 뒤편입니다. 제3공학관은 쪽문쪽 거대한 건물입니다.",
            "인문사회관": "운동장 근처에 있는 건물입니다.",
            "학생회관": "2층에 학생식당이 있습니다.",
            "대학본부": "학교 중앙에 위치한 건물입니다.",
            "학생성공관": "대학본부 뒤편에 위치한 건물입니다.",
            "농학관": "제2농학관은 학교 정문 바로 우측건물, 제1농학관은 학생회관 근처에 위치하고 있습니다.",
            "기계공학관": "기계공학관은 학교 후문에 위치하고 있습니다.",
            "공동실험실습관": "공동실험실습관은 제3공학관 근처에 위치하고 있습니다."
        }
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass

        return {d: "" for d in list("월화수목금")}

    def save_all_data(self, new_data):
        self.data.update(new_data)

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def respond(self, msg):
        if any(x in msg for x in ["보여줘", "보여줄래", "찐 시간표", "내 시간표"]):
            return "SIGNAL_SHOW_VISUAL"

        if any(x in msg for x in ["행사", "학사일정", "학교 일정", "일정표"]):
            return "SIGNAL_SHOW_EVENTS"

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
                if k in msg:
                    return f"📍 {k} 위치: {v}"

            return "정확한 건물명을 입력해주세요. 예: 공학관 어디야?"

        return "죄송해요, 그 말은 잘 이해하지 못했어요. 아래 가이드를 참고해 질문해주세요!"


class ChatGUI:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root

        root.title("한경국립대 나만의 학사비서")
        root.geometry("470x720")
        root.configure(bg="#2C3E50")

        self.log = scrolledtext.ScrolledText(
            root,
            width=52,
            height=28,
            bg="#ECF0F1",
            font=("맑은 고딕", 10),
            state="disabled"
        )
        self.log.pack(pady=10)

        f = tk.Frame(root, bg="#2C3E50")
        f.pack(fill="x", padx=10)

        self.ent = tk.Entry(f, width=34, font=("맑은 고딕", 11))
        self.ent.pack(side="left", padx=5, pady=5)
        self.ent.bind("<Return>", self.send)

        tk.Button(
            f,
            text="전송",
            command=self.send,
            bg="#3498DB",
            fg="white",
            width=8
        ).pack(side="left")

        tk.Button(
            root,
            text="📅 내 주간 시간표 한꺼번에 관리하기",
            command=self.open_batch_form,
            bg="#E67E22",
            fg="white",
            font=("맑은 고딕", 10, "bold")
        ).pack(fill="x", padx=15, pady=5)

        tk.Button(
            root,
            text="🏫 한경국립대 행사 월별 조회",
            command=self.open_hknu_event_calendar,
            bg="#9B59B6",
            fg="white",
            font=("맑은 고딕", 10, "bold")
        ).pack(fill="x", padx=15, pady=5)

        self.show_guide()

    def show_guide(self):
        guide = (
            "💡 [학사비서 사용법]\n"
            "• 학식/밥: 오늘의 학식 메뉴 확인\n"
            "• 날씨: 현재 학교(안성) 날씨 확인\n"
            "• 시간표/수업: 등록한 시간표 조회\n"
            "• 위치/어디: 건물 위치 안내\n"
            "• 행사/학사일정: 월별 학교 행사 캘린더 열기\n"
            "• '내 시간표 보여줘': 이미지 시간표 출력"
        )

        self.msg("시스템", guide)

    def send(self, e=None):
        txt = self.ent.get().strip()

        if txt:
            self.msg("나", txt)
            self.ent.delete(0, "end")

            response = self.bot.respond(txt)

            if response == "SIGNAL_SHOW_VISUAL":
                self.msg("챗봇", "요청하신 찐 시간표 이미지를 생성했습니다! 짜잔~ ✨")
                self.show_visual_timetable()

            elif response == "SIGNAL_SHOW_EVENTS":
                self.msg("챗봇", "한경국립대 행사 월별 조회 창을 열었습니다.")
                self.open_hknu_event_calendar()

            else:
                self.msg("챗봇", response)

            self.root.after(500, self.show_guide)

    def msg(self, sender, m):
        self.log.config(state="normal")
        self.log.insert("end", f"[{sender}]: {m}\n\n")
        self.log.config(state="disabled")
        self.log.yview("end")

    def show_visual_timetable(self):
        win = tk.Toplevel(self.root)
        win.title("나의 찐 시간표")
        win.geometry("650x450")
        win.configure(bg="#FDF6E3")

        tk.Label(
            win,
            text="시 간 표",
            font=("궁서", 35, "bold"),
            bg="#FDF6E3",
            fg="#333"
        ).pack(pady=20)

        table_frame = tk.Frame(win, bg="black", bd=2)
        table_frame.pack(padx=30, pady=10, fill="both", expand=True)

        days = list("월화수목금")

        for i, day in enumerate(days):
            tk.Label(
                table_frame,
                text=day,
                font=("맑은 고딕", 13, "bold"),
                bg="#D7D7D7",
                borderwidth=1,
                relief="solid",
                width=12,
                height=2
            ).grid(row=0, column=i, sticky="nsew")

        for i, day in enumerate(days):
            content = self.bot.data.get(day, "").replace("/", "\n").replace(" ", "\n")

            tk.Label(
                table_frame,
                text=content,
                font=("맑은 고딕", 11),
                bg="white",
                borderwidth=1,
                relief="solid",
                width=12,
                height=10,
                justify="center"
            ).grid(row=1, column=i, sticky="nsew")

        for i in range(5):
            table_frame.grid_columnconfigure(i, weight=1)

    def open_hknu_event_calendar(self):
        current = datetime.datetime.now()
        year = current.year
        month = current.month

        win = tk.Toplevel(self.root)
        win.title("한경국립대 월별 행사 조회")
        win.geometry("1080x760")
        win.configure(bg="#F8F9FA")

        title_label = tk.Label(
            win,
            text="",
            font=("맑은 고딕", 18, "bold"),
            bg="#F8F9FA"
        )
        title_label.pack(pady=10)

        button_frame = tk.Frame(win, bg="#F8F9FA")
        button_frame.pack()

        canvas = tk.Canvas(
            win,
            width=1040,
            height=560,
            bg="white",
            highlightthickness=0
        )
        canvas.pack(padx=15, pady=10)

        list_label = tk.Label(
            win,
            text="이번 달 행사 목록",
            font=("맑은 고딕", 12, "bold"),
            bg="#F8F9FA"
        )
        list_label.pack()

        list_text = tk.Text(
            win,
            height=7,
            font=("맑은 고딕", 10)
        )
        list_text.pack(fill="both", padx=15, pady=10)

        colors = [
            "#9B59B6",
            "#3498DB",
            "#27AE60",
            "#E67E22",
            "#E74C3C",
            "#16A085",
            "#2C3E50"
        ]

        def shorten_text(text, max_len=14):
            if len(text) > max_len:
                return text[:max_len] + "..."
            return text

        def render_calendar():
            nonlocal year, month

            canvas.delete("all")
            title_label.config(text=f"{year}년 {month}월 한경국립대 행사 캘린더")

            events = get_hknu_month_events(year, month)

            days = ["월", "화", "수", "목", "금", "토", "일"]

            canvas_width = 1040
            header_height = 40
            cell_width = canvas_width / 7
            cell_height = 82

            month_calendar = calendar.monthcalendar(year, month)

            while len(month_calendar) < 6:
                month_calendar.append([0, 0, 0, 0, 0, 0, 0])

            # 요일 헤더
            for col, day_name in enumerate(days):
                x1 = col * cell_width
                y1 = 0
                x2 = x1 + cell_width
                y2 = header_height

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#D6EAF8",
                    outline="black",
                    width=2
                )

                canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=day_name,
                    font=("맑은 고딕", 10, "bold")
                )

            day_position = {}

            # 날짜 칸 테두리만 그림
            for week_index, week in enumerate(month_calendar):
                for col, day in enumerate(week):
                    x1 = col * cell_width
                    y1 = header_height + week_index * cell_height
                    x2 = x1 + cell_width
                    y2 = y1 + cell_height

                    fill_color = "white" if day != 0 else "#F2F3F4"

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=fill_color,
                        outline="black",
                        width=2
                    )

                    if day != 0:
                        canvas.create_text(
                            x1 + 8,
                            y1 + 12,
                            text=str(day),
                            anchor="w",
                            font=("맑은 고딕", 10, "bold")
                        )

                        day_position[day] = (week_index, col)

            last_day = calendar.monthrange(year, month)[1]
            week_bar_count = {}

            # 행사 막대 그리기
            for event_index, event in enumerate(events):
                start_day = int(event.get("start_day", 1))
                end_day = int(event.get("end_day", start_day))
                title = event.get("title", "제목 없음")

                if end_day >= start_day:
                    display_start = max(1, start_day)
                    display_end = min(last_day, end_day)
                else:
                    display_start = max(1, start_day)
                    display_end = last_day

                color = colors[event_index % len(colors)]
                current_day = display_start

                while current_day <= display_end:
                    if current_day not in day_position:
                        current_day += 1
                        continue

                    week_index, start_col = day_position[current_day]
                    week = month_calendar[week_index]

                    end_col = start_col

                    for col in range(start_col, 7):
                        day_num = week[col]

                        if day_num == 0 or day_num > display_end:
                            break

                        end_col = col

                    span = end_col - start_col + 1

                    used_count = week_bar_count.get(week_index, 0)
                    bar_slot = used_count % 4
                    week_bar_count[week_index] = used_count + 1

                    x1 = start_col * cell_width + 4
                    x2 = (end_col + 1) * cell_width - 4

                    cell_top = header_height + week_index * cell_height
                    y1 = cell_top + 28 + bar_slot * 13
                    y2 = y1 + 11

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=color,
                        outline=color
                    )

                    canvas.create_text(
                        x1 + 6,
                        (y1 + y2) / 2,
                        text=shorten_text(title),
                        anchor="w",
                        fill="white",
                        font=("맑은 고딕", 8, "bold")
                    )

                    current_day = week[end_col] + 1

            # 하단 목록 표시
            list_text.delete("1.0", tk.END)

            if not events:
                list_text.insert(tk.END, "이번 달 등록된 학교 행사/학사일정이 없습니다.")
            else:
                for event in events:
                    list_text.insert(tk.END, f"{event['date']} - {event['title']}\n")

        def prev_month():
            nonlocal year, month

            month -= 1

            if month == 0:
                month = 12
                year -= 1

            render_calendar()

        def next_month():
            nonlocal year, month

            month += 1

            if month == 13:
                month = 1
                year += 1

            render_calendar()

        tk.Button(
            button_frame,
            text="◀ 이전 달",
            command=prev_month,
            bg="#95A5A6",
            fg="white"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="다음 달 ▶",
            command=next_month,
            bg="#95A5A6",
            fg="white"
        ).grid(row=0, column=1, padx=10)

        render_calendar()

    def open_batch_form(self):
        win = tk.Toplevel(self.root)
        win.title("주간 시간표 일괄 관리")
        win.geometry("380x480")
        win.configure(bg="#F3F4F6")

        tk.Label(
            win,
            text="[ 월~금 시간표 수정 ]",
            font=("맑은 고딕", 12, "bold"),
            bg="#F3F4F6"
        ).pack(pady=15)

        entry_widgets = {}

        for day in list("월화수목금"):
            row = tk.Frame(win, bg="#F3F4F6")
            row.pack(fill="x", padx=20, pady=5)

            tk.Label(
                row,
                text=f"{day}요일",
                width=6,
                bg="#F3F4F6"
            ).pack(side="left")

            ent = tk.Entry(row)
            ent.pack(side="left", fill="x", expand=True, padx=5)
            ent.insert(0, self.bot.data.get(day, ""))
            entry_widgets[day] = ent

        def save_all():
            new_data = {
                day: widget.get()
                for day, widget in entry_widgets.items()
            }

            self.bot.save_all_data(new_data)
            messagebox.showinfo("저장 완료", "주간 시간표가 모두 저장되었습니다!")
            self.msg("시스템", "전체 시간표가 업데이트 되었습니다.")
            win.destroy()
            self.show_guide()

        tk.Button(
            win,
            text="전체 저장하기",
            command=save_all,
            bg="#27AE60",
            fg="white",
            font=("", 10, "bold"),
            height=2
        ).pack(fill="x", padx=50, pady=15)

        tk.Button(
            win,
            text="📊 현재 시간표 이미지로 보기",
            command=self.show_visual_timetable,
            bg="#3498DB",
            fg="white"
        ).pack(fill="x", padx=50, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    ChatGUI(root, Team2_Bot())
    root.mainloop()

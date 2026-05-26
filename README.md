## 🚀 실행 방법 (Getting Started)

이 프로그램은 Python 3.10 이상 환경에서 정상 작동하며, 외부 라이브러리(`requests`, `beautifulsoup4`) 설치가 필요합니다.

### 1. 레포지토리 클론 및 이동
터미널(CMD)을 열고 아래 명령어를 입력하여 프로젝트를 다운로드하고 해당 디렉토리로 이동합니다.
```bash
git clone [https://github.com/yjs1217/chatBot_madebt_py.git](https://github.com/yjs1217/chatBot_madebt_py.git)
cd chatBot_madebt_py

###2. 필수 라이브러리 설치
실시간 학식 및 날씨 크롤링에 필요한 라이브러리를 설치합니다.

Bash
pip install requests beautifulsoup4
3. 프로그램 실행
메인 스크립트 파일을 실행하여 Tkinter GUI 챗봇을 구동합니다.

Bash
python main.py
(※ 만약 파일명이 main.py가 아니라면 실제 메인 파일명으로 변경하여 실행해 주세요.)

💾 데이터 완전히 저장하기 (Data Persistence & Usage)
본 프로그램은 사용자가 입력한 주간 시간표 데이터를 프로그램 종료 후에도 완벽하게 보존하기 위해 JSON 파일 기반의 로컬 데이터베이스를 사용합니다. 데이터 유실 없이 안전하게 사용하려면 아래 사항을 확인해 주세요.

1. 자동 데이터 생성 및 로드
프로그램을 처음 실행하면 실행 경로에 timetable.json 파일이 자동으로 생성됩니다.

사용자가 GUI 화면(시간표 일괄 관리 폼)을 통해 입력한 모든 스케줄은 실시간으로 이 JSON 파일에 기록됩니다.

이후 프로그램을 다시 껐다 켜더라도, 시스템이 자동으로 timetable.json을 읽어와 이전 데이터를 그대로 유지합니다.

2. ⚠️ 데이터 보존을 위한 중요 유의사항
정상 종료 권장: 데이터 파일 입출력 안정성을 위해, 프로그램 종료 시 터미널을 강제 종료(Ctrl + C)하기보다 Tkinter 윈도우 창의 닫기(X) 버튼을 눌러 정상 종료하는 것을 권장합니다.

디렉토리 권한: 프로그램이 실행되는 폴더에 파일 쓰기(Write) 권한이 있어야 timetable.json이 정상적으로 저장됩니다. (일반적인 환경에서는 문제없이 작동합니다.)

데이터 초기화 방법: 만약 전체 시간표 데이터를 완전히 초기화하고 처음부터 다시 입력하고 싶다면, 프로그램 종료 후 생성된 timetable.json 파일을 직접 삭제하고 재실행하시면 됩니다.


---

### 💡 팁
* 깃허브 README에 적용한 뒤, `timetable.json` 파일이 정상적으로 읽히고 쓰이는지 **실제 코드 상의 파일 경로 설정(`

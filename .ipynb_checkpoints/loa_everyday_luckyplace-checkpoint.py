import random
import datetime

# 추첨 대상 리스트
LUCKY_PLACES = [
    "🏇루테란 동부 - 루테란 성",
    "⚙️아르데타인 - 슈테른",
    "🗽베른 북부 - 베른 성",
    "🧚‍♀️로헨델 - 로아룬",
    "⚒️욘 - 위대한 성",
    "🐦‍⬛페이튼 - 칼라자 마을",
    "🏝️파푸니카 - 니아 마을",
    "🪽엘가시아 - 아리안오브",
    "🎨플레체 - 플레체",
    "🧪볼다이크 - 칼리나리",
    "👿쿠르잔 남부 - 엘네아드",
    "😸림레이크 남섬 - 샤",
]

# 캐시 저장용 전역 변수
_lucky_cache = {"date": None, "place": None}

def get_lucky_place():
    today = datetime.date.today()
    if _lucky_cache["date"] != today:
        _lucky_cache["date"] = today
        _lucky_cache["place"] = random.choice(LUCKY_PLACES)
    return f" 오늘의 재련 명당은...\n {_lucky_cache['place']} 입니다!"

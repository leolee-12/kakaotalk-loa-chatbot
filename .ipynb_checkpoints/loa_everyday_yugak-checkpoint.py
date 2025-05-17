import time

# 카카오톡 채팅방별 쿨타임 관리 딕셔너리
last_yugak_called_per_room = {}

def yugak_first_page_prices(chatroom_id):
    now = time.time()
    cooldown = 180  # 3분

    last_called = last_yugak_called_per_room.get(chatroom_id, 0)
    if now - last_called < cooldown:
        remaining = int(cooldown - (now - last_called))
        minutes = remaining // 60
        seconds = remaining % 60
        return f"⏳ 이 명령어는 해당 카카오톡방에서 {minutes}분 {seconds}초 후에 다시 사용 가능합니다."

    # 쿨타임 갱신
    last_yugak_called_per_room[chatroom_id] = now

    # 유물 각인서 검색 요청
    url = "https://developer-lostark.game.onstove.com/markets/items"
    payload = {
        'Sort': 'CURRENT_MIN_PRICE',
        'CategoryCode': 40000,
        'ItemGrade': '유물',
        'SortCondition': 'DESC'
    }

    search_result = api_post(url, payload)
    if not search_result:
        return "❌ 유물 각인서 데이터를 가져올 수 없습니다."

    item_list = search_result.get("Items", [])
    if not item_list:
        return "❌ 검색 결과가 없습니다."

    # 결과 생성
    result_lines = []
    for item in item_list:
        name = item.get("Name", "").replace("각인서", "").strip()
        price = item.get("CurrentMinPrice")

        if price and price > 0:
            result_lines.append(f"{name}: {price:,} 골드")
        else:
            result_lines.append(f"{name}: ❌ 등록된 매물 없음")

    return "\n".join(result_lines)

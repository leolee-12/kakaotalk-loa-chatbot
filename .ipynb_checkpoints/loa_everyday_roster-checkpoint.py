import re

from collections import defaultdict
from loa_everyday_init import *

def get_roster_info(name):
    # 입력 캐릭터의 전투정보실 프로필에서 서버 정보 확인
    profile_url = f"https://developer-lostark.game.onstove.com/armories/characters/{name}/profiles"
    profile = api_get(profile_url)
    if not profile or "ServerName" not in profile:
        return "❌ 캐릭터의 서버 정보를 불러올 수 없습니다."

    main_server = profile["ServerName"]

    # 원정대 캐릭터 목록 호출
    siblings_url = f"https://developer-lostark.game.onstove.com/characters/{name}/siblings"
    data = api_get(siblings_url)
    if not data:
        return "⚠️ 원정대 캐릭터 정보를 불러올 수 없습니다."

    # 서버별로 캐릭터 그룹핑
    server_dict = defaultdict(list)
    for char in data:
        try:
            server = char.get("ServerName", "Unknown")
            ilvl = float(char["ItemMaxLevel"].replace(",", ""))
            server_dict[server].append((char["CharacterName"], char["ItemMaxLevel"], ilvl))
        except:
            continue  # 값이 비정상적일 경우 건너뜀

    # 서버별로 출력 정리
    result_lines = []
    for server, chars in sorted(server_dict.items(), key=lambda x: (x[0] != main_server, x[0])):
        result_lines.append(f"🌐 서버: {server}")
        for name, level, _ in sorted(chars, key=lambda c: c[2], reverse=True):
            result_lines.append(f"  🔹 {name} - {level} Lv")

    return "\n".join(result_lines)

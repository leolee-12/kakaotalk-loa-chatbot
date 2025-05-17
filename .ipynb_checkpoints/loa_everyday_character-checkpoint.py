import requests
import re
import json
from urllib.parse import quote
from loa_everyday_init import HEADERS

# HTML 태그 제거 함수 (전역 사용 가능)
def strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "")

def get_character_info(name):
    encoded_name = quote(name)
    url = f"https://developer-lostark.game.onstove.com/armories/characters/{encoded_name}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        return "❌ API 요청 실패 (비공개 또는 존재하지 않음)"

    try:
        data = res.json()
    except Exception as e:
        return f"❌ 응답 파싱 오류: {e}"

    # 기본 정보
    profile = data.get("ArmoryProfile", {})
    character_name = profile.get("CharacterName", name)
    class_name = profile.get("CharacterClassName", "?")
    combat_level = profile.get("CharacterLevel", "?")
    ilvl = data.get("ItemMaxLevel") or profile.get("ItemAvgLevel", "?")
    server = profile.get("ServerName", "?")

    # 장비 정보
    armory_eq = data.get("ArmoryEquipment")
    if isinstance(armory_eq, dict) and "Equipment" in armory_eq:
        equipment = armory_eq["Equipment"]
    elif isinstance(armory_eq, list):
        equipment = armory_eq
    else:
        return "⚠️ 장비 데이터를 불러올 수 없습니다."

    # 무기 및 방어구
    weapon = next((e for e in equipment if "무기" in e.get("Type", "")), None)
    armors = [e for e in equipment if "무기" not in e.get("Type", "")]

    def extract_reinforce_info(item):
        """+재련 단계 + (상급 N단계) + [에스더] 표시"""
        name = item.get("Name", "")
        tooltip_raw = item.get("Tooltip", "")
        grade = item.get("Grade", "")

        # 재련 단계: +숫자
        reinforce_level = "?"
        m = re.search(r"\+(\d+)", name)
        if m:
            reinforce_level = f"+{m.group(1)}"

        # 상급 재련 단계
        supreme_text = ""
        try:
            tooltip_json = json.loads(tooltip_raw)
            el5 = tooltip_json.get("Element_005", {})
            value_field = el5.get("value", "") if isinstance(el5, dict) else el5
            clean_text = strip_html(value_field)
            m2 = re.search(r"(\d+)단계", clean_text)
            if m2:
                supreme_text = f"({m2.group(1)})"
        except Exception:
            pass

        # 에스더 무기 처리
        prefix = "에스더 " if grade == "에스더" else ""

        return f"{prefix}{reinforce_level} {supreme_text}".strip()

    weapon_str = extract_reinforce_info(weapon) if weapon else "무기 없음"
    armor_lvls = [extract_reinforce_info(a) for a in armors[:5]]

    # 보석
    gems = data.get("ArmoryGem", {}).get("Gems", [])
    gem_levels = {"겁화": [], "작열": []}
    for g in gems:
        name = strip_html(g.get("Name", ""))
        level = g.get("Level", "?")
        if "격" in name or "피해" in name or "겁화" in name:
            gem_levels["겁화"].append(str(level))
        elif "재사용" in name or "작열" in name:
            gem_levels["작열"].append(str(level))

    # 각인
    engraving_list = []
    engraving_data = data.get("ArmoryEngraving")
    if isinstance(engraving_data, dict):
        effects = engraving_data.get("Effects")
        if not effects or not isinstance(effects, list):
            effects = engraving_data.get("ArkPassiveEffects")
        if isinstance(effects, list):
            for e in effects:
                name = e.get("Name")
                if name:
                    clean_name = strip_html(name).strip()
                    if clean_name:
                        engraving_list.append(clean_name)
    if not engraving_list:
        engraving_list = ["없음"]

    # 아크 패시브 (ArkPassive → Points 대응)
    arc_points = {"진화": 0, "깨달음": 0, "도약": 0}
    ark_passive = data.get("ArkPassive")
    if isinstance(ark_passive, dict):
        points = ark_passive.get("Points")
        if isinstance(points, list):
            for p in points:
                name = strip_html(p.get("Name", "")).strip()
                value = int(p.get("Value", 0))
                if name in arc_points:
                    arc_points[name] = value

    # 최종 출력
    return f"""🧝 {character_name} ({class_name})
서버: {server}
전투 Lv.{combat_level} / 아이템 Lv.{ilvl}

🗡️ 무기: {weapon_str}
🛡️ 방어구: {' / '.join(armor_lvls)}

💎 보석
- 겁화: {' / '.join(gem_levels['겁화']) or '없음'}
- 작열: {' / '.join(gem_levels['작열']) or '없음'}

🔮 각인: {', '.join(engraving_list)}

🌟 아크 패시브
진화: {arc_points['진화']}pt / 깨달음: {arc_points['깨달음']}pt / 도약: {arc_points['도약']}pt
"""

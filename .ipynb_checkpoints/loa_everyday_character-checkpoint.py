def get_character_info(name):
    encoded_name = quote(name)
    url = f"https://developer-lostark.game.onstove.com/armories/characters/{encoded_name}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code == 404:
        return "❌ 존재하지 않거나, 장기간 미접속한 캐릭터입니다."
    elif res.status_code != 200:
        return "❌ API 요청 실패 (비공개 또는 오류 발생)"

    try:
        data = res.json()
        if data is None:
            return "❌ 캐릭터 정보가 없습니다 (비공개이거나 미등록된 캐릭터입니다)."
        if not isinstance(data, dict):
            return "❌ 응답 데이터 형식이 잘못되었습니다."
    except Exception as e:
        return f"❌ 응답 파싱 오류 또는 데이터 형식 문제: {e}\n(응답 본문: {res.text})"

    profile = data.get("ArmoryProfile")
    if not isinstance(profile, dict):
        return "❌ 캐릭터 정보가 없습니다 (비공개이거나 장기간 미접속한 캐릭터일 수 있습니다)."

    character_name = profile.get("CharacterName", name)
    class_name = profile.get("CharacterClassName", "?")
    combat_level = profile.get("CharacterLevel", "?")
    ilvl = data.get("ItemMaxLevel") or profile.get("ItemAvgLevel", "?")
    server = profile.get("ServerName", "?")

    # 무기 및 방어구
    armory_eq = data.get("ArmoryEquipment")
    if isinstance(armory_eq, dict) and "Equipment" in armory_eq:
        equipment = armory_eq["Equipment"]
    elif isinstance(armory_eq, list):
        equipment = armory_eq
    else:
        return "⚠️ 장비 데이터를 불러올 수 없습니다."

    weapon = next((e for e in equipment if "무기" in e.get("Type", "")), None)
    armors = [e for e in equipment if "무기" not in e.get("Type", "")]

    def extract_reinforce_info(item):
        name = item.get("Name", "")
        tooltip_raw = item.get("Tooltip", "")
        grade = item.get("Grade", "")
        reinforce_level = "?"
        m = re.search(r"\+(\d+)", name)
        if m:
            reinforce_level = f"+{m.group(1)}"
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
        prefix = "에스더 " if grade == "에스더" else ""
        return f"{prefix}{reinforce_level} {supreme_text}".strip()

    weapon_str = extract_reinforce_info(weapon) if weapon else "무기 없음"
    armor_lvls = [extract_reinforce_info(a) for a in armors[:5]]

    # 보석
    gem_levels = {"겁화": [], "작열": []}
    armory_gem = data.get("ArmoryGem")
    if armory_gem and isinstance(armory_gem, dict):
        raw_gems = armory_gem.get("Gems")
        if isinstance(raw_gems, list):
            for g in raw_gems:
                name = strip_html(g.get("Name", ""))
                level = g.get("Level", "?")
                if "격" in name or "피해" in name or "겁화" in name:
                    gem_levels["겁화"].append(str(level))
                elif "재사용" in name or "작열" in name:
                    gem_levels["작열"].append(str(level))

    # 각인 (AbilityStone 포함)
    engraving_list = []
    engraving_data = data.get("ArmoryEngraving")
    ark_effects = engraving_data.get("ArkPassiveEffects") if engraving_data else None

    if ark_effects and isinstance(ark_effects, list):
        for eff in ark_effects:
            name = eff.get("Name", "이름없음")
            grade = eff.get("Grade", "등급없음")
            level = eff.get("Level", 0)
            stone_level = eff.get("AbilityStoneLevel")

            line = f"{name} ({grade} {level}단계)"
            if stone_level is not None:
                line += f" [스톤 Lv {stone_level}]"
            engraving_list.append(line)

    if not engraving_list:
        engraving_list = ["없음"]

    # 아크 패시브
    arc_points = {"진화": 0, "깨달음": 0, "도약": 0}
    for p in data.get("ArkPassive", {}).get("Points", []):
        name = strip_html(p.get("Name", "")).strip()
        value = int(p.get("Value", 0))
        if name in arc_points:
            arc_points[name] = value

    # 출력
    output = f"""🧝 {character_name} ({class_name})
서버: {server}
전투 Lv.{combat_level} / 아이템 Lv.{ilvl}

🗡️ 무기: {weapon_str}
🛡️ 방어구: {' / '.join(armor_lvls)}

💎 보석
- 겁화: {' / '.join(gem_levels['겁화']) or '없음'}
- 작열: {' / '.join(gem_levels['작열']) or '없음'}

🔮 각인
{chr(10).join(['- ' + e for e in engraving_list])}

🌟 아크 패시브
진화: {arc_points['진화']}pt / 깨달음: {arc_points['깨달음']}pt / 도약: {arc_points['도약']}pt
"""

    # 이스터에그
    easter_eggs = {
        "이핼": "깝치지마라 From 이핼",
        "매일좋은날": "🌞 오늘도 좋은 하루 되세요! - From 매일좋은날",
        "러봇": "180.72.17 굵 (부심있음) ...",
        "구또슬": "떼굴떼굴떼굴"
    }

    if character_name in easter_eggs:
        output += f"\n\n{easter_eggs[character_name]}"

    return output

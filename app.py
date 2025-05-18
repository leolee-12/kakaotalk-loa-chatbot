from flask import Flask, request, Response
import json
from loa_everyday_character import get_character_info
from loa_everyday_roster import get_roster_info
from loa_everyday_yugak import yugak_first_page_prices
from loa_everyday_luckyplace import get_lucky_place
from loa_everyday_auction import calc_auction_price
from loa_everyday_gamble import run_gamble

app = Flask(__name__)

@app.route("/kakao", methods=["POST"])
def kakao_bot():
    try:
        data = request.get_json()

        # 기본 utterance 추출
        utterance = data.get("userRequest", {}).get("utterance", "").strip()

        # 슬롯 방식 우선 처리
        params = data.get("action", {}).get("params", {})
        char_name_slot = params.get("캐릭터명", "").strip()

        if char_name_slot:
            result = get_character_info(char_name_slot)

        elif utterance.startswith("/정보"):
            name = utterance.replace("/정보", "").strip()
            result = get_character_info(name)

        elif utterance.startswith("/원대"):
            name = utterance.replace("/원대", "").strip()
            result = get_roster_info(name)

        elif "/유각" in utterance:
            chatroom_id = data.get("userRequest", {}).get("user", {}).get("id", "default")
            result = yugak_first_page_prices(chatroom_id)

        elif utterance.startswith("/명당"):
            result = get_lucky_place()

        elif utterance.startswith("/경매"):
            try:
                number = int(utterance.replace("/경매", "").strip())
                if number <= 0:
                    result = "⚠️ 0보다 큰 숫자를 입력해주세요."
                else:
                    result = calc_auction_price(number)
            except ValueError:
                result = "⚠️ 숫자를 올바르게 입력해주세요. 예: `/경매 12345`"

        elif utterance.startswith("/도박"):
            result = run_gamble()

        else:
            result = "❓ 올바른 명령어를 입력해주세요."

        if not isinstance(result, str):
            result = "⚠️ 결과를 불러올 수 없습니다."

        response_data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText": {"text": result}}
                ]
            }
        }

        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )

    except Exception as e:
        error_text = f"❌ 서버 오류: {str(e)}"
        response_data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText": {"text": error_text}}
                ]
            }
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        ), 200

if __name__ == "__main__":
    app.run(debug=True)

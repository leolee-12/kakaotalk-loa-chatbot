from flask import Flask, request, Response
import json
from loa_everyday_character import get_character_info
from loa_everyday_roster import get_roster_info
from loa_everyday_yugak import yugak_first_page_prices

app = Flask(__name__)

@app.route("/kakao", methods=["POST"])
def kakao_bot():
    try:
        data = request.get_json()
        utterance = data.get("userRequest", {}).get("utterance", "").strip()

        if utterance.startswith("/정보"):
            name = utterance.replace("/정보", "").strip()
            result = get_character_info(name)
        elif utterance.startswith("/원대"):
            name = utterance.replace("/원대", "").strip()
            result = get_roster_info(name)
        elif "/유각" in utterance:
            chatroom_id = data.get("userRequest", {}).get("user", {}).get("id", "default")
            result = yugak_first_page_prices(chatroom_id)
        else:
            result = "❓ 올바른 명령어를 입력해주세요."

        # 안전한 문자열만 응답하도록 보장
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

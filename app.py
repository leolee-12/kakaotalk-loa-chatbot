from flask import Flask, request, jsonify
from loa_everyday_character import get_character_info
from loa_everyday_roster import get_roster_info
from loa_everyday_yugak import yugak_first_page_prices

app = Flask(__name__)

@app.route("/kakao", methods=["POST"])
def kakao_bot():
    data = request.get_json()
    utterance = data.get("userRequest", {}).get("utterance", "")

    if utterance.startswith("/정보"):
        name = utterance.replace("/정보", "").strip()
        result = get_character_info(name)
    elif utterance.startswith("/원대"):
        name = utterance.replace("/원대", "").strip()
        result = get_roster_info(name)
    elif "/유각" in utterance:
        result = yugak_first_page_prices()
    else:
        result = "❓ 올바른 명령어를 입력해주세요."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": result
                }
            }]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)

import requests

# ① API 키 입력
API_KEY = "censored"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# ② 공통 요청 함수 (응답 오류 체크 포함)
def api_get(url):
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"[ERROR] status code: {res.status_code}")
        return None

def api_post(url, payload):
    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"[ERROR] status code: {res.status_code}")
        return None

import requests

# ① API 키 입력
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDA1Nzc4NDEifQ.fLkoflAiyRgorFOtPK-0Q5Lpwr4wh1Y2sticFdsiNh-ksRKqdlaD7GxLzj5ABK_5tUTVjws7A6lIIg4fAilhTMt2hZlxVmksDlVRRAMYJaTpr2oa0CVd3U4Ch0bfsL9hrfAyQhnn5eBDrkGWk8k8JO6QAbd38usGWa78N5wswfENiqYFg9EaLVbgff0-1PHRK-K-BzMtJwBC3HfJBQciHN247sQfRW0dgSypsb4G1uORkwwudQrSOo528AHx5zYgE5wM2DmpdPt2eT5qZZwV4oXXZGiHRQchP4mimxMYc9NKp1KlAjEl3PrTSFjVTiOblVGtetuwADh8G8uXlbcFuQ"
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

import requests
import time


def predict_credit(payload):

    start = time.perf_counter()

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    elapsed = (time.perf_counter() - start) * 1000

    if response.status_code != 200:

        print("=" * 60)
        print("API ERROR")
        print("Status:", response.status_code)
        print(response.text)
        print("=" * 60)

    response.raise_for_status()

    result = response.json()

    result["response_time_ms"] = round(elapsed, 1)

    return result

def check_api_health():

    try:

        response = requests.get(
            "http://127.0.0.1:8000/health",
            timeout=2
        )

        return response.status_code == 200

    except Exception:

        return False
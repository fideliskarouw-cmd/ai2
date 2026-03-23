import requests

TELEGRAM_TOKEN = "8054207899:AAHThpS9RVdz663JzPobKOdPB6HdOnXr0H8"
OPENAI_API_KEY = "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"

def get_ai_response(user_text):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Kamu adalah AI yang sangat ramah, santai, dan pintar. Jelaskan hal sulit dengan cara sederhana seperti guru yang baik. Gunakan bahasa yang mudah dimengerti, kadang pakai emoji, tapi tetap jelas dan tidak bertele-tele."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()


def main():
    offset = None

    while True:
        updates = get_updates(offset)

        for update in updates["result"]:
            offset = update["update_id"] + 1

            try:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]

                reply = get_ai_response(text)
                send_message(chat_id, reply)

            except:
                pass


if __name__ == "__main__":
    main()
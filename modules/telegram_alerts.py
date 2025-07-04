import requests
import yaml
from datetime import datetime

config = yaml.safe_load(open("./config.yaml"))

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{config['telegram']['token']}/sendMessage"
        payload = {
            "chat_id": config['telegram']['channel'],
            "text": f"{datetime.now().strftime('%Y-%m-%d %H:%M')} {message}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {str(e)}")
import ntplib
import smtplib
import logging
import yaml
from datetime import datetime
from modules.telegram_alerts import send_alert

try:
    with open("./config.yaml", "r") as f:
        config = yaml.safe_load(f)
except Exception as e:
    logging.error(f"Ошибка загрузки config.yaml: {str(e)}")
    config = {
        "ntp_server": "pool.ntp.org",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    }


def check_network():
    results = {"ntp": False, "smtp": False}

    try:
        client = ntplib.NTPClient()
        response = client.request(config["ntp_server"], timeout=5)
        time_diff = abs(response.offset)
        results["ntp"] = time_diff < 5
        logging.info(f"NTP проверка: расхождение {time_diff:.2f} сек")
    except Exception as e:
        logging.error(f"NTP ошибка: {str(e)}")
        send_alert(f"⏰ NTP ошибка: {str(e)}")

    try:
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"], timeout=5) as server:
            server.starttls()
            server.ehlo()
            results["smtp"] = True
            logging.info("SMTP проверка: успешно")
    except Exception as e:
        logging.error(f"SMTP ошибка: {str(e)}")
        send_alert(f"📧 SMTP ошибка: {str(e)}")

    return results
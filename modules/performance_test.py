import subprocess
import time
from modules.telegram_alerts import send_alert
import yaml

config = yaml.safe_load(open("config.yaml"))

def run_disk_test():
    try:
        result = subprocess.run(
            ["dd", "if=/dev/zero", "of=./testfile", "bs=1G", "count=1", "oflag=direct"],
            stderr=subprocess.PIPE,
            text=True
        )
        speed = [l for l in result.stderr.split('\n') if 'MB/s' in l][0]
        send_alert(f"💾 Тест диска: {speed}")
        return speed
    except Exception as e:
        send_alert(f"❌ Ошибка теста диска: {str(e)}")
        return None

def run_network_test():
        try:
            import ping3
            latency = ping3.ping('8.8.8.8', unit='ms')
            if latency is not None:
                return f"{latency:.2f} ms"
            return "Timeout"
        except Exception as e:
            print(f"Ошибка теста сети: {str(e)}")
            return "FAIL"


import psutil
from modules.telegram_alerts import send_alert
import yaml

config = yaml.safe_load(open("config.yaml"))


def check_resources(config):
    metrics = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "vms": len([p for p in psutil.process_iter() if p.name() == "qemu-system-x86_64"])
    }

    alerts = []
    if metrics["cpu"] > config["thresholds"]["cpu"]:
        alerts.append(f"CPU перегруз: {metrics['cpu']}%")

    if metrics["ram"] > config["thresholds"]["ram"]:
        alerts.append(f"RAM перегруз: {metrics['ram']}%")

    if metrics["vms"] > config["thresholds"]["max_vms"]:
        alerts.append(f"Превышено количество ВМ: {metrics['vms']}")

    if alerts:
        send_alert("⚠️ ВМ тревога:\n" + "\n".join(alerts))

    return metrics
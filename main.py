import yaml

from modules.ml_predictor import predict_failure
from modules.vm_checks import check_resources
from modules.network_checks import check_network
from modules.ssl_check import check_ssl
from modules.performance_test import run_disk_test, run_network_test
from modules.vks_checks import check_vks_quality
from modules.voice_to_text import VoiceToText

config = yaml.safe_load(open("config.yaml"))

if __name__ == "__main__":
    print("[⚙️] Запуск проверок...")

    vm_status = check_resources(config)
    network_status = check_network()
    ssl_status = check_ssl(config["ssl"]["domains"][0])

    disk_speed = run_disk_test()
    network_latency = run_network_test()

    vks_status = check_vks_quality()
    vtt = VoiceToText()
    transcription = vtt.transcribe_audio("modules/test_audio.wav")

    ssl_info = f"Действует ещё {ssl_status['days_left']} дней" if ssl_status['valid'] else "Недействителен/ошибка"

    current_metrics = [vm_status["cpu"], vm_status["ram"]]
    ml_prediction = predict_failure(config, current_metrics)

    print("\n[📊] Отчёт:")
    print(f"- Ресурсы ВМ: CPU={vm_status['cpu']}%, RAM={vm_status['ram']}%")
    print(f"- Сеть: NTP={'OK' if network_status['ntp'] else 'FAIL'}, SMTP={'OK' if network_status['smtp'] else 'FAIL'}")
    print(f"- SSL: {ssl_info}")
    print(f"- ВКС: Аудио={vks_status['audio_quality']}%")
    print(f"- Голос в текст: {transcription or 'Ошибка'}")
    print(f"- Риск сбоя: {ml_prediction['risk']}% ({'Критический' if ml_prediction['is_critical'] else 'Нормальный'})")
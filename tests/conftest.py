import pytest

@pytest.fixture
def sample_config():
    return {
        "thresholds": {
            "cpu": 80,
            "ram": 85,
            "max_vms": 10,
            "disk": 90
        },
        "ssl": {
            "min_days": 30
        },
        "ml": {
            "model_path": "model.pkl",
            "training_data": "data.csv",
            "features": ["cpu_load", "ram_usage"],
            "threshold": 0.6
        },
        "smtp_server": "smtp.example.com",
        "ntp_server": "pool.ntp.org"
    }
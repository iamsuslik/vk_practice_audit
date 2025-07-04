import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import yaml
import os
from datetime import datetime, timedelta


def generate_training_data():
    timestamps = [datetime.now() - timedelta(days=i) for i in range(30)]
    cpu_load = np.random.randint(40, 100, size=30)
    ram_usage = np.random.randint(30, 95, size=30)
    failure = [1 if (cpu > 85 or ram > 80) else 0 for cpu, ram in zip(cpu_load, ram_usage)]

    data = pd.DataFrame({
        "timestamp": timestamps,
        "cpu_load": cpu_load,
        "ram_usage": ram_usage,
        "failure_occurred": failure
    })
    return data


def train_model(config):
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    if not os.path.exists(config["ml"]["training_data"]):
        data = generate_training_data()
        data.to_csv(config["ml"]["training_data"], index=False)
    else:
        data = pd.read_csv(config["ml"]["training_data"])

    X = data[config["ml"]["features"]]
    y = data["failure_occurred"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(model, config["ml"]["model_path"])
    print(f"Модель сохранена в {config['ml']['model_path']}")


def predict_failure(config, current_metrics):
    if not os.path.exists(config["ml"]["model_path"]):
        train_model(config)

    model = joblib.load(config["ml"]["model_path"])

    import pandas as pd
    features = pd.DataFrame([current_metrics],
                            columns=config["ml"]["features"])

    proba = model.predict_proba(features)[0][1]

    return {
        "risk": round(proba * 100, 2),
        "is_critical": proba > config["ml"]["threshold"]
    }


if __name__ == "__main__":
    config = yaml.safe_load(open("../config.yaml"))
    train_model(config)

    test_metrics = [90, 85]
    prediction = predict_failure(config, test_metrics)
    print(f"Результат прогноза: {prediction}")
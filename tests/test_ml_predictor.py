import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from modules.ml_predictor import predict_failure


def test_ml_prediction():
    mock_model = MagicMock()
    mock_model.predict_proba.return_value = [[0.3, 0.7]]

    with patch('joblib.load', return_value=mock_model), \
            patch('modules.ml_predictor.train_model'):

        config = {
            "ml": {
                "model_path": "model.pkl",
                "training_data": "data.csv",
                "threshold": 0.5,
                "features": ["cpu_load", "ram_usage"]
            }
        }

        test_data = pd.DataFrame([[80, 70]], columns=config["ml"]["features"])
        result = predict_failure(config, test_data.values[0])

        assert result["risk"] == 70.0
        assert result["is_critical"] is True
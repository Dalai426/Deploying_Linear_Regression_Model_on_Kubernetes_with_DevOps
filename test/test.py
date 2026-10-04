import json

import joblib
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
import numpy as np
import pytest
from fastapi.testclient import TestClient
from main import app


model = joblib.load("model/real_estate_model.pkl")
features_test, output_test = joblib.load("data/test_data.pkl")
client = TestClient(app)

def test_model_prediction():
    with open("model_evaluation_baseline.json", "r") as file:
        baseline = json.load(file)
    output_pred = model.predict(features_test)
    mae = mean_absolute_error(output_test, output_pred)
    mse = mean_squared_error(output_test, output_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(output_test, output_pred)

    baseline_mae = baseline["mae"]
    baseline_rmse = baseline["rmse"]
    baseline_r2 = baseline["r2"]

    assert mae <= baseline_mae, f"MAE too high: {mae}"
    assert rmse <= baseline_rmse, f"RMSE too high: {rmse}"
    assert r2 >= baseline_r2, f"R² too low: {r2}"

def test_predict():
    data = {
        "MedInc": 5.0,
        "HouseAge": 20.0,
        "AveRooms": 5.5,
        "AveBedrms": 1.0,
        "Population": 1000.0,
        "AveOccup": 3.0,
        "Latitude": 34.0,
        "Longitude": -118.0
    }

    response = client.post("/predict", json=data)

    assert response.status_code == 200

    result = response.json()

    assert "predicted_price" in result
    assert "predicted_price_millions" in result

    assert result["predicted_price"] > 0


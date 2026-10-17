from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd
import mlflow
from mlflow import sklearn as mlflow_sklearn

app = FastAPI(title="Real Estate Price Prediction API")

# Load trained model
MLFLOW_TRACKING_URI = "http://192.168.1.108:5001"
MLFLOW_REGISTRY_URI="http://192.168.1.108:5001"
MODEL_URI = "models:/RealEstateRandomForest@prod"


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(MLFLOW_REGISTRY_URI)
mlflow.set_experiment("real-estate-inference")
model = mlflow_sklearn.load_model(MODEL_URI)
print(type(model))

class HouseData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


@app.get("/")
def root():
    return {"message": "Real Estate Price Prediction API"}


@app.post("/predict")
@mlflow.trace(name="house-price-prediction")
def predict(house: HouseData):
    features = pd.DataFrame([{
        "MedInc": house.MedInc,
        "HouseAge": house.HouseAge,
        "AveRooms": house.AveRooms,
        "AveBedrms": house.AveBedrms,
        "Population": house.Population,
        "AveOccup": house.AveOccup,
        "Latitude": house.Latitude,
        "Longitude": house.Longitude
    }])

    prediction = model.predict(features)[0]
    
    # California Housing target is measured in $100,000s
    price = prediction * 100_000

    return {
        "predicted_price": round(float(price), 2),
        "predicted_price_millions": round(float(price / 1_000_000), 4)
    }
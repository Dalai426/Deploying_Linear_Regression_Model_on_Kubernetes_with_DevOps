from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd


app = FastAPI(title="Real Estate Price Prediction API")

# Load trained model
model = joblib.load("model/real_estate_model.pkl")


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
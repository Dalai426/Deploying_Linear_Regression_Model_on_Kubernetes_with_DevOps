from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
from typing import cast
from sklearn.datasets import fetch_california_housing
from sklearn.utils import Bunch
import os
import mlflow
from mlflow import sklearn as mlflow_sklearn
import optuna

# Connect to your Docker-hosted MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("ai-model")
    
with mlflow.start_run():
    data = cast(Bunch, fetch_california_housing(as_frame=True))

    features = data.data
    output = data.target

    print("Dataset loaded")
    print("Number of samples:", len(features))
    print("Features:", data.feature_names)

    features_train, features_test, output_train, output_test = train_test_split(
        features,
        output,
        test_size=0.2,
        random_state=42
    )
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)

    print("\nTraining samples:", len(features_train))
    print("Testing samples:", len(features_test))  

    model = LinearRegression()
    # The linear regression model has the same number of weights as features.
    print("\nTraining model...")
    model.fit(features_train, output_train)
    print("Training finished!")

    model_info = mlflow_sklearn.log_model(sk_model=model, name="trained_model")

    y_pred = model.predict(features_test[:5])
    print("Predicted:", y_pred)
    print("Actual:   ", output_test[:5].to_numpy())

    

    os.makedirs("data", exist_ok=True)
    os.makedirs("model", exist_ok=True)

    # Save test dataset
    joblib.dump(
        (features_test, output_test),
        "data/test_data.pkl"
    )

    joblib.dump(model, "model/real_estate_model.pkl")
    print("\nModel saved as model/real_estate_model.pkl")
    mlflow.set_tag("Training Info", "Basic LR model for housing data")

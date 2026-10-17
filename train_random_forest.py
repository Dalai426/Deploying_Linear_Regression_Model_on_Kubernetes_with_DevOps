from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from typing import cast
from sklearn.datasets import fetch_california_housing
from sklearn.utils import Bunch
import mlflow
from mlflow import sklearn as mlflow_sklearn
import optuna
from sklearn.metrics import mean_squared_error



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

def objective(trial):
    # Setting nested=True will create a child run under the parent run.
    with mlflow.start_run(nested=True, run_name=f"trial_{trial.number}") as child_run:
        rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32)
        rf_n_estimators = trial.suggest_int("rf_n_estimators", 50, 300, step=10)
        rf_max_features = trial.suggest_float("rf_max_features", 0.2, 1.0)
        params = {
            "max_depth": rf_max_depth,
            "n_estimators": rf_n_estimators,
            "max_features": rf_max_features,
        }
        # Log current trial's parameters
        mlflow.log_params(params)

        regressor_obj = RandomForestRegressor(**params)
        regressor_obj.fit(features_train, output_train)

        y_pred = regressor_obj.predict(features_test)
        error = mean_squared_error(output_test, y_pred)
        mlflow.log_metrics({"error": error})
        trial.set_user_attr("run_id", child_run.info.run_id)
        return error



mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("real-estate-random-forest-model")

with mlflow.start_run(run_name="study") as run:
    # Log the experiment settings
    n_trials = 10
    mlflow.log_param("n_trials", n_trials)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)

    # Log the best trial and its run ID
    mlflow.log_params(study.best_trial.params)
    mlflow.log_metrics({"best_error": study.best_value})
    if best_run_id := study.best_trial.user_attrs.get("run_id"):
        mlflow.log_param("best_child_run_id", best_run_id)
    best_params = {
        "max_depth": study.best_trial.params["rf_max_depth"],
        "n_estimators": study.best_trial.params["rf_n_estimators"],
        "max_features": study.best_trial.params["rf_max_features"],
    }
    final_model = RandomForestRegressor(**best_params)
    final_model.fit(features_train, output_train)
    model_info = mlflow_sklearn.log_model(
        sk_model=final_model,
        name="best_rf_model",
        skops_trusted_types=["sklearn.tree._tree.Tree"],
    )
    model_name = "RealEstateRandomForest"
    registered_model = mlflow.register_model(
        model_uri=model_info.model_uri,
        name=model_name,
    )
    client = mlflow.MlflowClient()
    client.set_registered_model_alias(
        name=model_name,
        alias="prod",
        version=registered_model.version,
    )
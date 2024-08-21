from celery import shared_task
import joblib
import io
import mlflow
import importlib
from entites.model_registry import MlflowRegistry
import pandas as pd


@shared_task(
    bind=True,
)
def load(self, model_name: str, backend: str, data):
    file_like_object = io.BytesIO(data)
    model = joblib.load(file_like_object)

    flavor = importlib.import_module("." + backend, "mlflow")

    mlflow.set_experiment(model_name)

    with mlflow.start_run() as run:
        flavor.log_model(model, "model")

    info = run.info

    metadata = {
        "run_id": info.run_id,
        "artifact_uri": info.artifact_uri,
        "run_name": info.run_name,
        "experiment_id": info.experiment_id,
    }

    return {"status": "success", "model": metadata}


@shared_task(
    bind=True,
)
def predict(self, model_name: str, data: dict = {}):

    model = MlflowRegistry(model_name)
    df_input = pd.DataFrame([data])
    result = model.predict(df_input)

    return result.tolist()

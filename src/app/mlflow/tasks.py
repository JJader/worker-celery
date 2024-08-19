from celery import shared_task
import joblib
import io
import mlflow
import importlib
import os

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
def predict(self, data=""):
    return f"ola mundo {data}"

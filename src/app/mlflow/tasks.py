from celery import shared_task
import joblib
import io
from entites.model_registry import PredictTask, MlflowRegistry
import pandas as pd


@shared_task(
    bind=True,
)
def load(self, model_name: str, backend: str, data):
    file_like_object = io.BytesIO(data)
    model = joblib.load(file_like_object)

    metadata = MlflowRegistry.load(model_name=model_name, backend=backend, model=model)

    return {"status": "success", "model": metadata}


@shared_task(
    bind=True,
    base=PredictTask,
)
def predict(self, model_name: str, data: dict = {}):

    df_input = pd.DataFrame([data])
    result = self.model.predict(df_input)

    data = {
        "result": result.tolist(),
        "model": self.model.model.metadata.__dict__,
    }

    return data

import mlflow
from mlflow.pyfunc import PyFuncModel
from entites.model_registry.base import ModelRegistry
from celery import Task
import importlib


class MlflowRegistry(ModelRegistry):
    def __init__(self, model_name: str) -> None:
        self.model_name: str = model_name
        self.experiment_id: str = self._get_experiment_id(model_name)
        self.run_id: str = None
        self.model: PyFuncModel = None

    @staticmethod
    def load(model_name: str, backend: str, model):

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

        return metadata

    def _get_experiment_id(self, model_name: str):
        experiment = dict(mlflow.get_experiment_by_name(model_name))
        return experiment["experiment_id"]

    def _get_latest_run_id(self):
        df = mlflow.search_runs(
            [self.experiment_id], order_by=["Created DESC"], max_results=1
        )

        latest_run_id = df.loc[0, "run_id"]
        return latest_run_id

    def _update_model_run_id(self, run_id):

        self.run_id = run_id
        logged_model = f"runs:/{run_id}/model"
        self.model = mlflow.pyfunc.load_model(logged_model)

    def predict(self, input):

        latest_run_id = self._get_latest_run_id()

        if self.run_id != latest_run_id:
            self._update_model_run_id(latest_run_id)

        return self.model.predict(input)


class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """

    abstract = True

    def __init__(self):
        super().__init__()
        self.model: MlflowRegistry = None
        self.model_name: str = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        latest_model_name = kwargs["model_name"]
        if not self.model or self.model_name != latest_model_name:
            self.model_name = latest_model_name
            self.model = MlflowRegistry(latest_model_name)

        print(args)
        print(kwargs)
        return self.run(*args, **kwargs)

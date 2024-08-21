import mlflow
from mlflow.pyfunc import PyFuncModel
from entites.model_registry.base import ModelRegistry


class MlflowRegistry(ModelRegistry):
    def __init__(self, model_name: str) -> None:
        self.model_name: str = model_name
        self.experiment_id: str = self._get_experiment_id(model_name)
        self.run_id: str = None
        self.model: PyFuncModel = None

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

        self._run_id = run_id
        logged_model = f"runs:/{run_id}/model"
        self.model = mlflow.pyfunc.load_model(logged_model)

    def predict(self, input):

        latest_run_id = self._get_latest_run_id()

        if self.run_id != latest_run_id:
            self._update_model_run_id(latest_run_id)

        return self.model.predict(input)

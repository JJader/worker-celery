from unittest.mock import MagicMock, patch
from mlflow.pyfunc import PyFuncModel
from src.entites.model_registry import MlflowRegistry  

@patch("mlflow.get_experiment_by_name")
def test_get_experiment_id(mock_get_experiment_by_name):
    # Configura o mock
    mock_experiment = {"experiment_id": "mock_experiment_id"}
    mock_get_experiment_by_name.return_value = mock_experiment

    registry = MlflowRegistry("test_model")
    experiment_id = registry._get_experiment_id("test_model")

    # Verifica o resultado
    assert experiment_id == "mock_experiment_id"


from unittest.mock import MagicMock, patch
from mlflow.pyfunc import PyFuncModel
from src.entites.model_registry import MlflowRegistry  

@patch("mlflow.set_experiment")
@patch("mlflow.start_run")
@patch("importlib.import_module")
def test_load(mock_import, mock_start_run, mock_set_experiment):
    # Configura os mocks
    mock_run = MagicMock()
    mock_run.info.run_id = "mock_run_id"
    mock_run.info.artifact_uri = "mock_artifact_uri"
    mock_run.info.run_name = "mock_run_name"
    mock_run.info.experiment_id = "mock_experiment_id"
    mock_start_run.return_value.__enter__.return_value = mock_run

    mock_flavor = MagicMock()
    mock_import.return_value = mock_flavor

    model = MagicMock()
    metadata = MlflowRegistry.load("test_model", "test_backend", model)

    # Verifica se os dados retornados estão corretos
    expected_metadata = {
        "run_id": "mock_run_id",
        "artifact_uri": "mock_artifact_uri",
        "run_name": "mock_run_name",
        "experiment_id": "mock_experiment_id"
    }
    assert metadata == expected_metadata

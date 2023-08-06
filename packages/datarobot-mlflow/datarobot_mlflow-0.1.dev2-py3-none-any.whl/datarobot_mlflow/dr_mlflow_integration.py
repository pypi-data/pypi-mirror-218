import json
import logging
from pprint import pformat

import mlflow

from datarobot_mlflow import DataRobotKeyValueHelper, KVEntityType, KVValueType


class Model:
    def __init__(self):
        self.name = None
        self.run_id = None
        self.description = None
        self.tags = {}
        self.metrics = {}
        self.parameters = {}
        self.artifacts = []

    def __str__(self):
        s = "Name: {} run_id: {}\n".format(self.name, self.run_id)
        s += "description:\n{}".format(self.description) + "\n"
        s += "tags: " + pformat(self.tags) + "\n"
        s += "parameters: " + pformat(self.parameters) + "\n"
        s += "metrics: " + pformat(self.metrics) + "\n"
        s += "artifacts" + pformat(self.artifacts) + "\n"
        return s


class DataRobotMLFlowIntegration:
    """
    A class to provide helper functions to integrate Datarobot and MLFlow
    """

    DRFLOW_MODEL_DESCRIPTION_TAG = "drflow.model.description"
    DRFLOW_RUN_ID_TAG = "drflow.model.run_id"
    MLFLOW_MODEL_HISTORY_TAG = "mlflow.log-model.history"

    def __init__(
        self,
        mlflow_model_registry_uri: str = None,
        datarobot_uri: str = None,
        datarobot_token: str = None,
        artifacts_local_dir: str = "/tmp",
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._mlflow_model_registry_uri = mlflow_model_registry_uri
        self._datarobot_uri = datarobot_uri
        self._datarobot_token = datarobot_token
        self._artifacts_local_dir = artifacts_local_dir

        mlflow.set_tracking_uri(self._mlflow_model_registry_uri)
        mlflow.set_registry_uri(self._mlflow_model_registry_uri)
        self._mlflow_client = mlflow.MlflowClient()

    def _list_model_versions(self):
        for mv in self._mlflow_client.search_model_versions():
            self._logger.debug("\n----- listed model ----")
            mv_dict = dict(mv)
            self._logger.debug(pformat(mv_dict, indent=4))

    def _find_model_version(self, model_name, model_version):
        # TODO: find a better api call to get the version info
        for mv in self._mlflow_client.search_model_versions(
            "name='{}'".format(model_name)
        ):
            self._logger.debug("\n----- searched model -----")
            mv_dict = dict(mv)
            self._logger.debug(pformat(mv_dict, indent=4))
            if int(mv.version) == int(model_version):
                return mv
        return None

    def _handle_artifacts(self, run_id, model, with_artifacts, with_model):
        self._logger.debug("Artifacts:")
        artifact_list = self._mlflow_client.list_artifacts(run_id)
        self._logger.debug(pformat(artifact_list))

        model_artifacts_dir = None
        if self.MLFLOW_MODEL_HISTORY_TAG in model.tags:
            print("Found history tag")
            print(model.tags[self.MLFLOW_MODEL_HISTORY_TAG])

            history_json = json.loads(model.tags[self.MLFLOW_MODEL_HISTORY_TAG])
            print(pformat(history_json))

        else:
            print("History tag not found")

        model_artifact = None
        for fi in artifact_list:
            self._logger.debug(
                "Size: {size} path: {path}".format(size=fi.file_size, path=fi.path)
            )
            model_fi = {
                "path": fi.path,
                "local_path": None,
                "is_dir": fi.is_dir,
                "file_size": fi.file_size,
                "artifact_type": KVValueType.path_to_artifact_type(fi.path),
            }
            model.artifacts.append(model_fi)
            self._logger.debug(f"{with_artifacts} {with_model}")
            if with_artifacts:
                if with_model is True or fi.is_dir is False:
                    self._logger.debug(f"Downloading artifact: {fi.path}")
                    local_path = mlflow.artifacts.download_artifacts(
                        run_id=run_id,
                        artifact_path=fi.path,
                        dst_path=self._artifacts_local_dir,
                    )
                    model_fi["local_path"] = local_path

    def get_mlflow_model(
        self,
        model_name: str,
        model_version: str,
        with_artifacts: bool = False,
        with_model: bool = False,
        model_dir: str = None,
    ) -> Model:
        """
        Getting an MLFlow model as a Model object
        :param model_name: The model name to retrieve
        :param model_version: The model version to retrieve
        :param with_artifacts: If True download artifacts locally
        :param with_model: If True download model as well.
        :param model_dir: Directory where to save model artifacts if found
        :return: A Model object
        """
        model = Model()
        model.name = model_name
        mv = self._find_model_version(model_name, model_version)
        if mv is None or mv.run_id is None:
            raise Exception("Could not find model version or a valid run_id")

        model.description = mv.description
        model.run_id = mv.run_id

        run = self._mlflow_client.get_run(mv.run_id)
        self._logger.debug(pformat(run.data))

        self._logger.debug("Parameters:")
        self._logger.debug(pformat(run.data.params))
        model.parameters = run.data.params.copy()

        self._logger.debug("Metrics:")
        self._logger.debug(pformat(run.data.metrics))
        model.metrics = run.data.metrics.copy()

        self._logger.debug("Tags:")
        self._logger.debug(pformat(run.data.tags))
        model.tags = run.data.tags.copy()

        self._handle_artifacts(mv.run_id, model, with_artifacts, with_model)
        return model

    def set_datarobot_model_metadata(
        self, model: Model, datarobot_model_id: str, verbose_fh=None, prefix=""
    ):
        """
        Given a model object sync all metadata with a DataRobot model in the registry
        :param model:
        :param datarobot_model_id:
        :param verbose_fh:
        :param prefix: Add prefix to all kv names
        :return:
        """
        drkv = DataRobotKeyValueHelper(
            datarobot_uri=self._datarobot_uri,
            datarobot_token=self._datarobot_token,
            entity_id=datarobot_model_id,
            entity_type=KVEntityType.MODEL_PACKAGE,
        )

        print(
            "Setting model metadata in DataRobot:", file=verbose_fh
        ) if verbose_fh else False

        for key, value in model.parameters.items():
            key = prefix + key
            print(
                "setting parameter: {}".format(key), file=verbose_fh
            ) if verbose_fh else False
            drkv.set_parameter(key, value)

        for key, value in model.metrics.items():
            key = prefix + key
            print(
                "setting metric: {}".format(key), file=verbose_fh
            ) if verbose_fh else False
            drkv.set_metric(key, value)

        for key, value in model.tags.items():
            key = prefix + key
            print(
                "setting tag: {}".format(key), file=verbose_fh
            ) if verbose_fh else False
            drkv.set_tag(key, value)

        for fi in model.artifacts:
            if fi["local_path"] and fi["artifact_type"] is not None:
                name = prefix + fi["path"]
                print(
                    "setting artifact: {}".format(name), file=verbose_fh
                ) if verbose_fh else False
                drkv.set_artifact(
                    name, fi["local_path"], artifact_type=fi["artifact_type"]
                )

        print(
            "setting description as {} tag".format(self.DRFLOW_MODEL_DESCRIPTION_TAG),
            file=verbose_fh,
        ) if verbose_fh else False
        drkv.set_tag(self.DRFLOW_MODEL_DESCRIPTION_TAG, model.description)

        print(
            "setting run id as {} tag".format(self.DRFLOW_RUN_ID_TAG), file=verbose_fh
        ) if verbose_fh else False
        drkv.set_tag(self.DRFLOW_RUN_ID_TAG, model.run_id)

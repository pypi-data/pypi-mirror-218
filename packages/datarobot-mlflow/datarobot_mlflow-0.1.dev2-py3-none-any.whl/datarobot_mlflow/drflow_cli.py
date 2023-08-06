import argparse
import logging
import os
import sys
from collections import defaultdict

from datarobot_mlflow import (
    DataRobotKeyValueHelper,
    DataRobotMLFlowIntegration,
    KVCategory,
    KVEntityType,
    are_service_principal_credentials_valid,
)


class CLIActions:
    SYNC = "sync"
    DELETE_ALL_DR_KEYS = "delete-all-dr-keys"
    LIST_DR_KEYS = "list-dr-keys"
    LIST_MLFLOW_KEYS = "list-mlflow-keys"
    DOWNLOAD_MLFLOW_MODEL = "download-mlflow-model"
    VALIDATE_AUTH = "validate-auth"

    @staticmethod
    def all_actions_values():
        return [
            m
            for v, m in vars(CLIActions).items()
            if not (v.startswith("_") or callable(m))
        ]


class CLIAuthTypes:
    AZURE_SERVICE_PRINCIPAL = "azure-service-principal"

    @classmethod
    def all(cls):
        return [cls.AZURE_SERVICE_PRINCIPAL]


class CLIServiceProviderTypes:
    AZURE_DATABRICKS = "azure-databricks"

    @classmethod
    def all(cls):
        return [cls.AZURE_DATABRICKS]


class DRFlowCLI:
    MLOPS_TOKEN_ENV = "MLOPS_API_TOKEN"
    DESC_STR = """
    Export model metadata from MLFLow and update DataRobot model to have these metadata
    """

    def __init__(self):
        pass

    def list_all_kv_in_dr(self, drkv: DataRobotKeyValueHelper):
        all_kv = drkv.get_all_kv()
        print(all_kv)
        kv_by_category = defaultdict(list)
        for kv in all_kv:
            kv_by_category[kv["category"]].append(kv)

        print()
        print("Training Parameters:")
        for kv in kv_by_category[KVCategory.TRAINING_PARAMETER]:
            print("{name:20} {value:20}".format(name=kv["name"], value=kv["value"]))

        print()
        print("Metrics:")
        for kv in kv_by_category[KVCategory.METRIC]:
            print("{name:20} {value:20}".format(name=kv["name"], value=kv["value"]))

        print()
        print("Tags:")
        for kv in kv_by_category[KVCategory.TAG]:
            print("{name:20} {value:20}".format(name=kv["name"], value=kv["value"]))

        print()
        print("Artifacts:")
        for kv in kv_by_category[KVCategory.ARTIFACT]:
            print("{name:20} {value:20}".format(name=kv["name"], value=kv["value"]))

    def list_mlflow_keys(
        self, drflow: DataRobotMLFlowIntegration, mlflow_model, mlflow_model_version
    ):
        model = drflow.get_mlflow_model(
            mlflow_model, mlflow_model_version, with_artifacts=False
        )
        if not model:
            print("Error getting model from MLFlow")
            return
        print("----- MLFlow Model Info -----")
        print(model)

    def parse_args(self, args, action_list, default_action):
        parser = argparse.ArgumentParser(description=DRFlowCLI.DESC_STR)
        parser.add_argument("--mlflow-registry", help="URI of MLFlow registry")
        parser.add_argument("--mlflow-model", help="MLFlow model name")
        parser.add_argument("--mlflow-model-version", help="MLFlow model version")
        parser.add_argument("--mlflow-url", help="MLFlow URL")
        parser.add_argument("--dr-model", help="DataRobot model id")
        parser.add_argument("--dr-url", help="DataRobot URL")
        parser.add_argument("--dr-token", help="Datarobot User token", default=None)
        parser.add_argument(
            "--with-artifacts",
            action="store_true",
            default=False,
            help="Also sync artifacts",
        )
        parser.add_argument(
            "--prefix", default="", help="Add prefix to all DataRobot Key Values"
        )
        parser.add_argument(
            "--verbose", action="store_const", default=None, const=sys.stdout
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="Set logger to basic config and debug level",
        )
        parser.add_argument(
            "--action",
            default=default_action,
            choices=action_list,
            help=f"Action to run. Choose from: {action_list}",
        )
        parser.add_argument(
            "--model-dir", help="Path to a directory to use for saving MLFlow model"
        )
        parser.add_argument(
            "--service-provider-type",
            choices=CLIServiceProviderTypes.all(),
            help="Define type of service provider to use",
        )
        parser.add_argument(
            "--auth-type",
            choices=CLIAuthTypes.all(),
            help="Define type of authentication to use",
        )

        options = parser.parse_args(args=args)

        if not options.dr_token:
            options.dr_token = os.environ.get(DRFlowCLI.MLOPS_TOKEN_ENV, None)
            if options.dr_token is None:
                print(
                    "Datarobot token was not provided via an argument and could not detect "
                    f"{DRFlowCLI.MLOPS_TOKEN_ENV} in environment"
                )
                exit(1)
        return options

    def run(self, args=None):
        options = self.parse_args(
            args=args,
            action_list=CLIActions.all_actions_values(),
            default_action=CLIActions.SYNC,
        )

        if options.debug:
            logging.basicConfig(level=logging.DEBUG)

        # validating credentials exits early and does not use MLflow client
        if options.action == CLIActions.VALIDATE_AUTH:
            if options.auth_type is None:
                raise Exception("--validate-auth requires --auth-type to be defined")
            if options.service_provider_type is None:
                raise Exception(
                    "--validate-auth requires --service-provider-type to be defined"
                )
            if options.auth_type == CLIAuthTypes.AZURE_SERVICE_PRINCIPAL:
                if are_service_principal_credentials_valid():
                    print(
                        "Azure AD Service Principal credentials are valid for obtaining access token"
                    )
                else:
                    print(
                        "Azure AD Service Principal credentials are not valid; check environment variables"
                    )
                return
            else:
                print(
                    "Authentication type '{}' is not supported for --validate-auth".format(
                        options.auth_type
                    )
                )
                return

        # TODO: add ability to add only new items or update
        # option_allow_update_of_kv = False

        drkv = DataRobotKeyValueHelper(
            datarobot_uri=options.dr_url,
            datarobot_token=options.dr_token,
            entity_id=options.dr_model,
            entity_type=KVEntityType.MODEL_PACKAGE,
        )

        drflow = DataRobotMLFlowIntegration(
            mlflow_model_registry_uri=options.mlflow_url,
            datarobot_uri=options.dr_url,
            datarobot_token=options.dr_token,
        )

        if options.action == CLIActions.DELETE_ALL_DR_KEYS:
            drkv.delete_all_kv()
        elif options.action == CLIActions.LIST_MLFLOW_KEYS:
            self.list_mlflow_keys(
                drflow,
                mlflow_model=options.mlflow_model,
                mlflow_model_version=options.mlflow_model_version,
            )
        elif options.action == CLIActions.LIST_DR_KEYS:
            self.list_all_kv_in_dr(drkv)
        elif options.action == CLIActions.DOWNLOAD_MLFLOW_MODEL:
            if options.model_dir is None:
                raise Exception(
                    "no model directory argument was provided, this is required"
                    " when downloading an MLFlow mode"
                )
            model = drflow.get_mlflow_model(
                options.mlflow_model,
                options.mlflow_model_version,
                with_artifacts=options.with_artifacts,
                with_model=True,
                model_dir="/tmp/bbb",
            )
            if not model:
                raise Exception("Error getting model from MLFlow")
            print(f"Model is located at: {options.model_dir}")

        elif options.action == CLIActions.SYNC:
            if options.mlflow_url is None:
                raise Exception("Must provide MLFlow URL arg, see --help output")
            if options.mlflow_model is None:
                raise Exception("Must provide MLFlow model name, see --help output")
            if options.mlflow_model_version is None:
                raise Exception("Must provide MLFlow model version, see --help output")

            if options.verbose:
                print(f"Getting model from MLFlow at: {options.mlflow_url}")
            model = drflow.get_mlflow_model(
                options.mlflow_model,
                options.mlflow_model_version,
                with_artifacts=options.with_artifacts,
            )
            if not model:
                raise Exception("Error getting model from MLFlow")
            if options.verbose:
                print("----- MLFlow Model Info -----")
                print(model)
                print()
                print("Synchronizing MLFlow metadata with DataRobot model metadata")
            drflow.set_datarobot_model_metadata(
                model,
                options.dr_model,
                prefix=options.prefix,
                verbose_fh=options.verbose,
            )
        else:
            print("Action [{}] is not supported".format(options.action))


def main():
    test_args = [
        # "--action", "delete-all-dr-keys",
        # "--action", "list-mlflow-keys",
        "--action",
        "download-mlflow-model",
        "--model-dir",
        "/tmp/model-d",
        "--mlflow-model",
        "diabetes-1",
        "--mlflow-model-version",
        "1",
        "--mlflow-url",
        "http://localhost:8080",
        "--dr-model",
        "639ae0711cc55ec4fb6fca12",
        "--dr-url",
        "https://staging.datarobot.com",
        "--with-artifacts",
        # "--prefix", "bricks.",
        "--verbose",
        "--debug",
    ]

    drflow_cli = DRFlowCLI()
    use_test_args = os.environ.get("DRFLOW_CLI_USE_TEST_ARGS", None)
    if use_test_args is not None:
        print("Using TEST arguments: {}", test_args)
        args = test_args
    else:
        args = None
    drflow_cli.run(args=args)


if __name__ == "__main__":
    main()

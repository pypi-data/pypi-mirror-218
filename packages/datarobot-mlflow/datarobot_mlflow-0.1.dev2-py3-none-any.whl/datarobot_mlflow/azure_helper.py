#  Copyright (c) 2023 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.

"""
To authenticate with an Azure AD Service Principal:
* configure the Service Principal (app registration) in Azure
* export the following environment variables as defined for the Service Principal:
export AZURE_TENANT_ID="<directory_aka_tenant_id>"
export AZURE_CLIENT_ID="<application_aka_client_id>"
export AZURE_CLIENT_SECRET="<client_secret>"
"""

import logging
import os

import requests

# hardcoded scope for all Azure Databricks installations
SCOPE_AZURE_DATABRICKS = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"

TENANT_ID_KEY = "AZURE_TENANT_ID"
CLIENT_ID_KEY = "AZURE_CLIENT_ID"
CLIENT_SECRET_KEY = "AZURE_CLIENT_SECRET"
REQUIRED_SERVICE_PRINCIPAL_ENV_VARS = [TENANT_ID_KEY, CLIENT_ID_KEY, CLIENT_SECRET_KEY]

logger = logging.getLogger(__name__)


def are_service_principal_credentials_valid():
    """
    Test generating an access token based on Service Principal credentials.
    Return True or False based on success.
    """
    for var in REQUIRED_SERVICE_PRINCIPAL_ENV_VARS:
        if not os.getenv(var):
            logger.error(f"Required environment variable is not defined: {var}")
    tenant_id = os.getenv(TENANT_ID_KEY)
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": os.getenv(CLIENT_ID_KEY),
        "grant_type": "client_credentials",
        "scope": SCOPE_AZURE_DATABRICKS,
        "client_secret": os.getenv(CLIENT_SECRET_KEY),
    }
    response = requests.post(url, data=payload)
    if response.ok:
        access_token = response.json().get("access_token")
        return bool(access_token)
    else:
        return False

__author__ = 'Klera DevOps'
__version__ = '0.0.3'

import json

from google.cloud import compute_v1
from google.oauth2 import service_account
from gcp_cis.gcp_cis_checks_iam import iam_controls
from gcp_cis.gcp_cis_checks_logging_and_monitoring import logging_monitoring_controls
from gcp_cis.gcp_cis_checks_networking import networking_controls
from gcp_cis.gcp_cis_checks_storage import storage_controls
from gcp_cis.gcp_cis_checks_vms import vms_controls


class gcp_client(iam_controls, logging_monitoring_controls, networking_controls, storage_controls, vms_controls):
    def __init__(self, service_account_path: str, project_number, org_id=None):
        """
        :param service_account_path:
        :param org_id:
        """
        self.scopes = ['https://www.googleapis.com/auth/cloud-platform']
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_path, scopes=self.scopes
        )
        self.organization_id = org_id

        sa_file = open(service_account_path)
        sa = json.load(sa_file)

        self.project_id = sa['project_id']

        region_client = compute_v1.RegionsClient(credentials=self.credentials)
        region_list = region_client.list(project=self.project_id)
        self.locations = [region.name for region in region_list]

        super().__init__(self.scopes, self.credentials, self.organization_id, self.project_id, self.locations, project_number)

    def getCompliance(self) -> list:
        """
        :return: list of GCP CIS Benchmarks
        """
        compliance_data = []

        compliance_data.extend(self.get_iam_compliance())
        compliance_data.extend(self.get_logging_monitoring_compliance())
        compliance_data.extend(self.get_networking_compliance())
        compliance_data.extend(self.get_vms_compliance())
        compliance_data.extend(self.get_storage_compliance())

        return compliance_data

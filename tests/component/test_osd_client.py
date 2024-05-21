from http import HTTPStatus
import json
import unittest
from os import getenv

import requests

from ska_oso_pht_services.api_clients.osd_api import osd_client

from tests.unit.util import VALID_OSD_GET_OSD_CYCLE1_RESULT_JSON, assert_json_is_equal

KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
OSD_API_URL = getenv(
    "OSD_API_URL",
    "https://k8s.stfc.skao.int/{KUBE_NAMESPACE}/osd/api/v1/osd",
)


class TestOSDCLIENT(unittest.TestCase):
    # def make_request_to_get_osd_endpoint(self, _cycle_id):
    #     c = osd_client
    #     try:
    #         osd_data = c.get_osd(_cycle_id)
    #         return osd_data
    #     except osd_client.APIError as err:
    #         return str(err)

    def test_get_osd(self):
        cycle_id = 1

        result = requests.get(f"{OSD_API_URL}?cycle_id={cycle_id}")

        #result = self.make_request_to_get_osd_endpoint(cycle_id)
        assert result.status_code == HTTPStatus.OK
        assert_json_is_equal(json.dumps(result), VALID_OSD_GET_OSD_CYCLE1_RESULT_JSON)

    # def test_get_osd_unvalid_cycle(self):
    #     cycle_id = "dhfjdhfjdhfjd"
    #     result = self.make_request_to_get_osd_endpoint(cycle_id)
    #     assert result == "An error occurred: 400"

import json
import unittest

from ska_oso_pht_services.api_clients.osd_api import osd_client

from tests.unit.util import VALID_OSD_GET_OSD_CYCLE1_RESULT_JSON, assert_json_is_equal


class TestOSDCLIENT(unittest.TestCase):
    def make_request_to_get_osd_endpoint(self, _cycle_id):
        c = osd_client
        try:
            osd_data = c.get_osd(_cycle_id)
            return osd_data
        except osd_client.APIError as err:
            return str(err)

    def test_get_osd(self):
        cycle_id = 1
        result = self.make_request_to_get_osd_endpoint(cycle_id)
        assert_json_is_equal(json.dumps(result), VALID_OSD_GET_OSD_CYCLE1_RESULT_JSON)

    # def test_get_osd_unvalid_cycle(self):
    #     cycle_id = "dhfjdhfjdhfjd"
    #     result = self.make_request_to_get_osd_endpoint(cycle_id)
    #     assert result == "An error occurred: 400"

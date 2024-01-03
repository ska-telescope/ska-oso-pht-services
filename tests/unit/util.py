"""
Utility functions to be used in tests
"""
import json
import os.path

from deepdiff import DeepDiff
from ska_oso_pdm.entities.common.sb_definition import SBDefinition
from ska_oso_pdm.schemas import CODEC


def assert_json_is_equal(json_a, json_b):
    """
    Utility function to compare two JSON objects
    """
    # key/values in the generated JSON do not necessarily have the same order
    # as the test string, even though they are equivalent JSON objects, e.g.,
    # subarray_id could be defined after dish. Ensure a stable test by
    # comparing the JSON objects themselves.
    obj_a = json.loads(json_a)
    obj_b = json.loads(json_b)
    try:
        assert obj_a == obj_b
    except AssertionError as exc:
        # raise a more useful exception that shows *where* the JSON differs
        diff = DeepDiff(obj_a, obj_b, ignore_order=True)
        raise AssertionError(f"JSON not equal: {diff}") from exc


def load_string_from_file(filename):
    """
    Return a file from the current directory as a string
    """
    cwd, _ = os.path.split(__file__)
    path = os.path.join(cwd, filename)
    with open(path, "r", encoding="utf-8") as json_file:
        json_data = json_file.read()
        return json_data


VALID_MID_SBDEFINITION_JSON = load_string_from_file("testfile_sample_mid_sb.json")
valid_mid_sbdefinition = CODEC.loads(SBDefinition, VALID_MID_SBDEFINITION_JSON)

INVALID_MID_SBDEFINITION_JSON = CODEC.dumps(
    SBDefinition(sbd_id="sbi-mvp01-20200325-00001")
)

VALID_MOCKED_DATA_JSON = load_string_from_file("testfile_sample_data.json")
VALID_MOCKED_DATA_LIST_JSON = load_string_from_file(
    "testfile_sample_data_get_list.json"
)

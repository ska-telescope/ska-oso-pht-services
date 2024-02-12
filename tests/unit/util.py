"""
Utility functions to be used in tests
"""
import json
import os.path

from deepdiff import DeepDiff


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


VALID_MOCKED_DATA_JSON = load_string_from_file("testfile_sample_data.json")
VALID_MOCKED_DATA_LIST_JSON = load_string_from_file(
    "testfile_sample_data_get_list.json"
)
VALID_PROPOSAL_DATA_JSON = load_string_from_file("testfile_sample_proposal.json")
VALID_PROPOSAL_FRONTEND_CREATE_JSON = load_string_from_file("testfile_frontend_create_proposal.json")
VALID_PROPOSAL_FRONTEND_UPDATE_JSON = load_string_from_file("testfile_frontend_update_proposal.json")

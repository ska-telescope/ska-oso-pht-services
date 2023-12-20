"""
Utilities for ska_oso_pdm.schemas tests.
"""
import json

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

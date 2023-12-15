"""
Unit tests for the ska_oso_pdm.entities.scan_definition module.
"""

from datetime import timedelta

from ska_oso_pdm.entities.common.scan_definition import ScanDefinition

mid_scandef_1 = ScanDefinition(
    scan_definition_id="id_42",
    scan_duration=timedelta(hours=14.6),
    target_beam_configuration_ids=None,
    scan_type_id="science",
    dish_configuration_id="dish config 123",
    target_id="science_A",
    csp_configuration_id="csp_id_41",
)
# mid_scandef_2 = ScanDefinition(
#     "id_42",
#     timedelta(seconds=52560),
#     "typical",
#     None,
#     "dish config 123",
#     "science_A",
#     "csp_id_41",
# )
#
# mid_scandef_3 = ScanDefinition(
#     "id_43",
#     timedelta(hours=14.6),
#     "typical",
#     None,
#     "dish config 123",
#     "science_A",
#     "csp_id_41",
# )
#
# low_scandef_1 = ScanDefinition(
#     "id_42", timedelta(hours=14.6), "typical", ["beam 1", "beam 2"], None, None, None
# )
#
# low_scandef_2 = ScanDefinition(
#     "id_42", timedelta(seconds=52560), "typical", ["beam 1", "beam 2"], None, None, None
# )
#
# low_scandef_3 = ScanDefinition(
#     "id_42", timedelta(hours=14.6), "typical", ["beam 1", "beam 3"], None, None, None
# )
#
# mid_scandef_4 = ScanDefinition(
#     14.6, "atypical", "dish config 123", "science_A", "csp_id_41", "id_42"
# )
# mid_scandef_5 = ScanDefinition(
#     14.6, "typical", "dish config XYZ", "science_A", "csp_id_41", "id_42"
# )
# mid_scandef_6 = ScanDefinition(
#     14.6, "atypical", "dish config 123", "science_A", "csp_id_XX", "id_42"
# )
# mid_scandef_7 = ScanDefinition(
#     14.6, "typical", "dish config 123", "calibration_B", "csp_id_41", "id_42"
# )
#
#
# def test_scan_definition_eq():
#     """
#     Verify that ScanDefinition objects are considered equal when:
#      - they have the same id
#       - they have the same scan duration
#       - they have the same dish (MID) or target beam (LOW) configuration id(s)
#     """
#
#     assert mid_scandef_1 == mid_scandef_2
#     assert mid_scandef_1 != mid_scandef_3
#     assert mid_scandef_1 != low_scandef_1
#     assert low_scandef_1 == low_scandef_2
#     assert low_scandef_1 != low_scandef_3
#     assert mid_scandef_1 != mid_scandef_4
#     assert mid_scandef_1 != mid_scandef_5
#     assert mid_scandef_1 != mid_scandef_6
#     assert mid_scandef_1 != mid_scandef_7
#
#
# def test_scan_definition_is_not_equal_to_other_objects():
#     """
#     Verify that ScanDefinition objects are considered unequal to other objects.
#     """
#
#     assert mid_scandef_1 != object
#     assert low_scandef_1 != object
#
#
# def test_repr():
#     """
#     Verify that __repr__ for a Mid and Low ScanDefinition is implemented correctly
#     """
#
#     mid_expected = (
#         "<ScanDefinition('id_42', 14:36:00, typical, None, "
#         "science_A, dish config 123, csp_id_41)>"
#     )
#     low_expected = (
#         "<ScanDefinition('id_42', 14:36:00, typical, ['beam 1', "
#         "'beam 2'], None, None, None)>"
#     )
#
#     assert repr(mid_scandef_1) == mid_expected
#     assert repr(low_scandef_1) == low_expected

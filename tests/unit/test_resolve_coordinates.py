import sys
import os
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/ska_oso_pht_services/utils'))
sys.path.insert(0, module_path)
import pytest
from unittest.mock import patch
from astroquery.simbad import Simbad
from astroquery.ipac.ned import Ned

from resolve_coordinates import convert_deg_to_hms, get_coordinates






# Mocking Simbad and Ned responses for testing
simbad_mock_result = {'RA': ['05 34 30.9'], 'DEC': ['+22 00 53']}
ned_mock_result = {'RA(deg)': [83.62875], 'DEC(deg)': [22.01472222]}

@pytest.mark.parametrize("degrees, expected_result", [
    (0, (0, 0, 0.0)),
    (15, (1, 0, 0.0)),
    (30, (2, 0, 0.0)),
    (45, (3, 0, 0.0)),
    (60, (4, 0, 0.0)),
])
def test_convert_deg_to_hms(degrees, expected_result):
    result = convert_deg_to_hms(degrees)
    assert result == expected_result

@patch('astroquery.simbad.Simbad.query_object', return_value=simbad_mock_result)
@patch('astroquery.ned.Ned.query_object', return_value=None)
def test_get_coordinates_simbad_found(simbad_mock, ned_mock):
    result = get_coordinates("TestObject")
    expected_coordinates = "05:34:30.9 +22:00:53"
    assert result == expected_coordinates

@patch('astroquery.simbad.Simbad.query_object', return_value=None)
@patch('astroquery.ned.Ned.query_object', return_value=ned_mock_result)
def test_get_coordinates_ned_found(simbad_mock, ned_mock):
    result = get_coordinates("TestObject")
    expected_coordinates = "5h 34m 30.90s 22d 0m 53.00s" 
    assert result == expected_coordinates

@patch('astroquery.simbad.Simbad.query_object', return_value=None)
@patch('astroquery.ned.Ned.query_object', return_value=None)
def test_get_coordinates_not_found(simbad_mock, ned_mock):
    result = get_coordinates("NonExistentObject")
    assert result == "Not found"

@patch('astroquery.simbad.Simbad.query_object', side_effect=Exception("Simbad error"))
@patch('astroquery.ned.Ned.query_object', return_value=None)
def test_get_coordinates_error_simbad(simbad_mock, ned_mock):
    result = get_coordinates("ErrorObject")
    assert result == "Error fetching coordinates"

@patch('astroquery.simbad.Simbad.query_object', return_value=None)
@patch('astroquery.ned.Ned.query_object', side_effect=Exception("NED error"))
def test_get_coordinates_error_ned(simbad_mock, ned_mock):
    result = get_coordinates("ErrorObject")
    assert result == "Error fetching coordinates"

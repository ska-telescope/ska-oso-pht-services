import pytest
from unittest.mock import MagicMock, patch
from src.ska_oso_pht_services.utils.resolve_coordinates import convert_deg_to_hms, get_coordinates

# Mocking astroquery.simbad.Simbad.query_object
@patch('astroquery.simbad.Simbad.query_object')
def test_get_coordinates_simbad(mock_query_object):
    mock_query_object.return_value = MagicMock()
    mock_query_object.return_value['RA'] = ['05 34 30.9']
    mock_query_object.return_value['DEC'] = ['+22 00 53']

    result = get_coordinates('M42')
    assert result == '05:34:30.9 +22:00:53'

# Mocking astroquery.ned.Ned.query_object
@patch('astroquery.ned.Ned.query_object')
def test_get_coordinates_ned(mock_query_object):
    mock_query_object.return_value = MagicMock()
    mock_query_object.return_value['RA(deg)'] = [83.62925]
    mock_query_object.return_value['DEC(deg)'] = [22.014722]

    result = get_coordinates('M31')
    assert result == '05h 34m 34.62s 22d 00m 53.00s'

# Test case for conversion function
def test_convert_deg_to_hms():
    result = convert_deg_to_hms(83.62925)
    assert result == (5, 34, 34.62)

# Test case for object not found in both databases
@patch('astroquery.simbad.Simbad.query_object')
@patch('astroquery.ned.Ned.query_object')
def test_get_coordinates_not_found(mock_ned_query, mock_simbad_query):
    mock_simbad_query.return_value = None
    mock_ned_query.return_value = None

    result = get_coordinates('NonexistentObject')
    assert result == 'Not found'

# Test case for error handling
@patch('astroquery.simbad.Simbad.query_object')
def test_get_coordinates_error(mock_query_object):
    mock_query_object.side_effect = Exception('Connection Error')

    result = get_coordinates('M101')
    assert result == 'Error fetching coordinates'

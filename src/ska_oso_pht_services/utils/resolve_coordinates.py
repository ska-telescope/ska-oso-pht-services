from astroquery.ipac.ned import Ned
from astroquery.simbad import Simbad


def convert_deg_to_hms(degrees):
    """
    Convert degrees to hours, minutes, and seconds format.

    Parameters:
    degrees (float): Value in degrees to convert.

    Returns:
    tuple: Hours, minutes, and seconds.
    """
    hours = int(degrees / 15)  # 1 hour = 15 degrees
    remainder = (degrees / 15 - hours) * 60
    minutes = int(remainder)
    seconds = (remainder - minutes) * 60
    return hours, minutes, seconds


def convert_deg_to_dms(degrees):
    """
    Convert degrees to degree, minutes, and seconds format.

    Parameters:
    degrees (float): Value in degrees to convert.

    Returns:
    tuple: Degree, minutes, and seconds.
    """
    degree = int(degrees)
    remainder = abs(degrees - degree) * 60
    minutes = int(remainder)
    seconds = (remainder - minutes) * 60
    return degree, minutes, seconds


def get_coordinates(name: str) -> str:
    """
    Retrieve formatted coordinates (RA and DEC) for a given astronomical object name.
    Queries Simbad first, and if no results are found, queries NED.
    Converts RA and DEC from degrees to hours, minutes, and seconds.

    Parameters:
    name (str): Name or identifier of the astronomical object to query.

    Returns:
    str: Formatted coordinates (e.g., '05h:34:30.9s +22:00:53s').
    If the object is not found in both databases, returns 'Not found'.
    If an error occurs during the query process, returns 'Error fetching coordinates'.
    """
    try:
        # Query Simbad first
        result_table = Simbad.query_object(name)
        if result_table is not None:
            ra = result_table["RA"][0]
            dec = result_table["DEC"][0]
            # Format coordinates with colons instead of spaces
            coordinates = f"{ra.replace(' ', ':')} {dec.replace(' ', ':')}"
            return coordinates

        # If not found in Simbad, query NED
        ned_data = Ned.query_object(name)
        if ned_data is not None:
            ra_degrees = ned_data["RA(deg)"][0]
            dec_degrees = ned_data["DEC(deg)"][0]

            # Convert RA and DEC degrees to hours, minutes, and seconds
            ra_hours, ra_minutes, ra_seconds = convert_deg_to_hms(ra_degrees)
            dec_hours, dec_minutes, dec_seconds = convert_deg_to_dms(dec_degrees)

            # Format coordinates in hours, minutes, and seconds
            coordinates = (
                f"{ra_hours}h {ra_minutes}m {ra_seconds:.2f}s {dec_hours}d"
                f" {dec_minutes}m {dec_seconds:.2f}s"
            )
            return coordinates

        return "Not found"

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error fetching coordinates"

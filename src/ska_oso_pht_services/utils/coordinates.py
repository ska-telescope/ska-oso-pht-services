import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.ipac.ned import Ned
from astroquery.simbad import Simbad
from astropy.coordinates import Angle



def get_coordinates(object_name):
    """
    Query celestial coordinates for a given object name from SIMBAD and NED databases.
    If the object is not found in SIMBAD database
    it then queries the NED (NASA/IPAC Extragalactic Database).
    The function returns the Right Ascension (RA)
    and Declination (Dec) in the hour-minute-second (HMS) and
    degree-minute-second (DMS) format respectively.
    Parameters:
    object_name (str): name of the celestial object to query.
    Returns:
    string: RA in HMS format Dec in DMS format
    or a 'not found' message.
    """
    # Try searching in SIMBAD
    result_table_simbad = Simbad.query_object(object_name)
    if result_table_simbad is not None:
        ra = result_table_simbad["RA"][0]
        dec = result_table_simbad["DEC"][0]
    else:
        # If not found in SIMBAD, search in NED
        result_table_ned = Ned.query_object(object_name)
        if result_table_ned is None or len(result_table_ned) == 0:
            return "Object not found in SIMBAD or NED"
        ra = result_table_ned["RA"][0]
        dec = result_table_ned["DEC"][0]

    # Creating a SkyCoord object
    coordinates = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))

    # Formatting RA and DEC in HMS and DMS
    ra_hms = coordinates.ra.to_string(unit=u.hour, sep=":")
    dec_dms = coordinates.dec.to_string(unit=u.degree, sep=":")

    return f"{ra_hms} {dec_dms}"







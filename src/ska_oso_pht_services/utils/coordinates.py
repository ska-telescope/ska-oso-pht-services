import astropy.units as u
from astropy.coordinates import SkyCoord, Angle
from astroquery.ipac.ned import Ned
from astroquery.simbad import Simbad
from astroquery.exceptions import RemoteServiceError


def round_coord_to_3_decimal_places(ra, dec):
    """
    Rounds the seconds component of RA and the arcseconds component of DEC to 3 decimal places.

    Parameters:
    - ra (str): Right Ascension in "HH:MM:SS.sssssssss"
    - dec (str): Declination in "DD:MM:SS.sssssssss"

    Returns:
    - tuple: RA and DEC coordinates with seconds and arcseconds rounded to 3 decimal places.
    """
    ra_formatted = ':'.join(f"{round(float(x), 3):06.3f}" if i == 2 else x for i, x in enumerate(ra.split(':')))
    dec_formatted = ':'.join(f"{round(float(x), 3):06.3f}" if i == 2 else x for i, x in enumerate(dec.split(':')))
    return ra_formatted, dec_formatted


def convert_to_galactic(ra, dec):
    """
    Converts RA and DEC coordinates to Galactic coordinates.

    Parameters:
    - ra (str): The Right Ascension in the format "HH:MM:SS.sss"
    - dec (str): The Declination in the format "+DD:MM:SS.sss"

    Returns:
    - str: The Galactic coordinates as a string (l, b)
    """
    # Creating a SkyCoord object with the given RA and DEC
    coord = SkyCoord(ra, dec, frame='icrs', unit=(u.hourangle, u.deg))
    
    # Converting to Galactic frame
    galactic_coord = coord.galactic
    
    # Formatting the output
    longitude = galactic_coord.l.to_string(unit=u.degree, decimal=True)
    latitude = galactic_coord.b.to_string(unit=u.degree, decimal=True)
    
    return (longitude, latitude)


def get_coordinates(object_name, coordinate_system):
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
        try:
            result_table_ned = Ned.query_object(object_name)
        except RemoteServiceError as e:
            return f"{'Object not found in SIMBAD or NED', e}"
        ra = result_table_ned["RA"][0]
        dec = result_table_ned["DEC"][0]

    # Creating a SkyCoord object
    coordinates = (SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame='icrs')
                   .fk5.to_string('hmsdms').replace('h', ':')
                   .replace('d', ':').replace('m', ':').replace('s', ''))
    if coordinate_system.lower() == "galactic":
        return convert_to_galactic(coordinates.split(" ")[0], coordinates.split(" ")[1])
    else:
        return round_coord_to_3_decimal_places(coordinates.split(" ")[0], coordinates.split(" ")[1])
        




def convert_ra_dec_deg(ra_str, dec_str):
    """
    Convert RA and Dec from sexagesimal (string format) to decimal degrees.

    Parameters:
    ra_str (str): RA in the format "HH:MM:SS" (e.g., "5:35:17.3")
    dec_str (str): Dec in the format "DD:MM:SS" (e.g., "-1:2:37")

    Returns:
    tuple: RA and Dec in decimal degrees
    """
    ra = Angle(ra_str, unit=u.hour)
    dec = Angle(dec_str, unit=u.deg)

    return [round(ra.degree, 3), round(dec.degree, 3)]
            


print(get_coordinates("M1", "galactic"))
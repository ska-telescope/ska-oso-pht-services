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
    ra_hours, ra_minutes, ra_seconds = ra.split(":")
    ra_seconds_round = round(float(ra_seconds), 3)
    ra_formatted = f"{ra_hours}:{ra_minutes}:{ra_seconds_round:06.3f}"

    dec_hours, dec_minutes, dec_seconds = dec.split(":")
    dec_seconds_round = round(float(dec_seconds), 3)
    dec_formatted = f"{dec_hours}:{dec_minutes}:{dec_seconds_round:06.3f}"

    return {"ra": ra_formatted, 
    "dec" : dec_formatted}


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

    return {"ra": round(ra.degree, 3), 
    "dec" : round(dec.degree, 3)}
            


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
    
    return  {"longitude" :longitude, 
        "latitude":latitude}


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
    coordinate_system = "galactic"

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
    coordinates = (SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame='icrs')
                   .fk5.to_string('hmsdms').replace('h', ':')
                   .replace('d', ':').replace('m', ':').replace('s', ''))
    return {"ra" : coordinates.split(" ")[0], "dec" : coordinates.split(" ")[1]}

   


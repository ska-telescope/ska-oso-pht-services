import math

class CoordinateConverter:
    """
    A class for converting equatorial coordinates to galactic coordinates.
    """

    @staticmethod
    def parse_ra_dec(ra_str, dec_str):
        """
        Parses HH:mm:ss and DD:mm:ss strings to degrees.

        Args:
        - ra_str (str): Right Ascension string in HH:mm:ss format.
        - dec_str (str): Declination string in DD:mm:ss format.

        Returns:
        - float: Right Ascension in degrees.
        - float: Declination in degrees.
        """
        try:
            ra_parts = list(map(float, ra_str.split(':')))
            dec_parts = list(map(float, dec_str.split(':')))
            
            ra_deg = 15 * (ra_parts[0] + ra_parts[1]/60 + ra_parts[2]/3600)
            
            sign = -1 if dec_parts[0] < 0 else 1
            dec_deg = abs(dec_parts[0]) + dec_parts[1]/60 + dec_parts[2]/3600
            dec_deg *= sign
            
            return ra_deg, dec_deg
        except ValueError:
            raise ValueError("Invalid input format. Use HH:mm:ss for RA and DD:mm:ss for Dec.")

    @staticmethod
    def equatorial_to_galactic(ra_str, dec_str):
        """
        Converts equatorial coordinates (RA and Dec) to galactic coordinates (l and b).

        Args:
        - ra_str (str): Right Ascension string in HH:mm:ss format.
        - dec_str (str): Declination string in DD:mm:ss format.

        Returns:
        - float: Galactic Longitude (l) in degrees.
        - float: Galactic Latitude (b) in degrees.
        """
        try:
            ra_deg, dec_deg = CoordinateConverter.parse_ra_dec(ra_str, dec_str)
            
            ra_rad = math.radians(ra_deg)
            dec_rad = math.radians(dec_deg)

            sin_b = (math.sin(dec_rad) * math.sin(math.radians(62.8717)) +
                     math.cos(dec_rad) * math.cos(math.radians(62.8717)) * math.cos(ra_rad - math.radians(282.8595)))

            b = math.degrees(math.asin(sin_b))

            tan_l = (math.sin(ra_rad - math.radians(282.8595)) * math.cos(dec_rad)) / \
                    (math.cos(dec_rad) * math.sin(math.radians(62.8717)) - 
                     math.sin(dec_rad) * math.cos(math.radians(62.8717)) * math.cos(ra_rad - math.radians(282.8595))))

            l = math.degrees(math.atan(tan_l)) + 33
            if l < 0:
                l += 360

            return l, b
        except ValueError:
            raise ValueError("Invalid input format or values for RA and Dec.")


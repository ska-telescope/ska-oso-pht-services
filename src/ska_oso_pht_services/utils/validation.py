import astropy.units as u
from astropy.coordinates import SkyCoord

# from ska_oso_pht_services.api_clients.osd_api import osd_client

# TODO: use values from OSD after connection is ready


def _search_objects_by_key(objects, key, value):
    for obj in objects:
        if key in obj and obj[key] == value:
            return obj
    return None

def _calculate_dec(lat, min_elevation):
    return lat - 90 + min_elevation, 90 - lat - min_elevation


def validate_proposal(proposal) -> dict:
    """
    validate targets in a proposal

    Makes use of the get_osd() function to fetch the OSD data for a specified cycle ID.

    Parameters:
    proposal_str (str): proposal

    Returns:
    dict: result of validation and messages
    """

    # TODO use osd_data when ready
    # c = osd_client
    # osd_data = c.get_osd(1)  
    # TODO: replace hard coded cycle id by a parameter

    lat_low = -26.82472208
    lat_mid = -30.712925
    min_ele = 15  # TODO: replace when OSD is in place in our backend

    result = True

    messages = []
    try:
        # TODO: use Proposal data model from pdm
        targets_in_degree = []
        for target in proposal["proposal_info"]["targets"]:
            if target["reference_coordinate"]["kind"] == "equatorial":
                # check if dec is string/decimal
                if isinstance(target["reference_coordinate"]["dec"], str):
                    skycoord_ra_dec = SkyCoord(
                        f'{target["reference_coordinate"]["ra"]}{target["reference_coordinate"]["dec"]}',  # noqa: E501
                        unit=(u.hourangle, u.deg),
                    )
                    dec_to_decimal = skycoord_ra_dec.dec.degree
                else:
                    dec_to_decimal = target["reference_coordinate"]["dec"]

                targets_in_degree.append(
                    {"target_name": target["target_name"], "dec": dec_to_decimal}
                )
            elif target["reference_coordinate"]["kind"] == "galactic":
                targets_in_degree.append(
                    {"target_name": target["target_name"], 
                    "dec": float(SkyCoord(l=target["reference_coordinate"]["lon"] * u.degree, \
                            b=target["reference_coordinate"]["lat"] * u.degree, frame="galactic")
                            .transform_to("icrs").dec.to_string(decimal=True, unit=u.degree))})

        for obs in proposal["proposal_info"]["observation_set"]:
            for linked_source in obs["linked_sources"]:
                target_detail = _search_objects_by_key(
                    targets_in_degree, "target_name", linked_source
                )

                if target_detail is None:
                    result = False
                    messages.append(
                        f'Target {linked_source} in Observation {obs["obset_id"]} is'
                        " not found in proposal target"
                    )
                else:
                    if obs["array"] == "MID":
                        dec_min_mid, dec_max_mid = _calculate_dec(lat_mid, min_ele)
                        if (
                            target_detail["dec"] < dec_min_mid
                            or target_detail["dec"] > dec_max_mid
                        ):
                            result = False
                            messages.append(
                                f"Target {linked_source} with declination:"
                                f' {target_detail["dec"]} in Observation'
                                f' {obs["obset_id"]} is out of range'
                            )
                    elif obs["array"] == "LOW":
                        dec_min_low, dec_max_low = _calculate_dec(lat_low, min_ele)
                        if (
                            target_detail["dec"] < dec_min_low
                            or target_detail["dec"] > dec_max_low
                        ):
                            result = False
                            messages.append(
                                f"Target {linked_source} with declination:"
                                f' {target_detail["dec"]} in Observation'
                                f' {obs["obset_id"]} is out of range'
                            )
    except ValueError as err:
        messages.append(str(err))
        return {"result": False, "validation_errors": messages}

    return {"result": result, "validation_errors": messages}

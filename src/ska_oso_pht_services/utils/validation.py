import astropy.units as u
from astropy.coordinates import SkyCoord

# TODO: use values from OSD after connection is ready


def _search_objects_by_key(objects, key, value):
    for obj in objects:
        if key in obj and obj[key] == value:
            return obj
    return None


def _convert_galactic_to_equatorial_and_get_dec(lat, lon):
    gc = SkyCoord(l=lon * u.degree, b=lat * u.degree, frame="galactic")
    return float(gc.transform_to("icrs").dec.to_string(decimal=True, unit=u.degree))


def validate_proposal(proposal) -> dict:
    """
    validate targets in a proposal

    Parameters:
    proposal_str (str): proposal

    Returns:
    dict: result of validation and messages
    """

    lat_low = -26.82472208
    lat_mid = -30.712925
    min_ele = 15  # TODO: replace when OSD is in place in our backend

    dec_min_low = lat_low - 90 + min_ele
    dec_max_low = 90 - lat_low - min_ele

    dec_min_mid = lat_mid - 90 + min_ele
    dec_max_mid = 90 - lat_mid - min_ele

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
                        f'{target["reference_coordinate"]["ra"]}{target["reference_coordinate"]["dec"]}',
                        unit=(u.hourangle, u.deg),
                    )
                    dec_to_decimal = skycoord_ra_dec.dec.degree
                else:
                    dec_to_decimal = target["reference_coordinate"]["dec"]

                targets_in_degree.append(
                    {"target_name": target["target_name"], "dec": dec_to_decimal}
                )
            elif target["reference_coordinate"]["kind"] == "galactic":
                dec = _convert_galactic_to_equatorial_and_get_dec(
                    target["reference_coordinate"]["lat"],
                    target["reference_coordinate"]["lon"],
                )
                targets_in_degree.append(
                    {"target_name": target["target_name"], "dec": dec}
                )

        for obs in proposal["proposal_info"]["observation_set"]:
            for linked_source in obs["linked_sources"]:
                print(linked_source)
                target_detail = _search_objects_by_key(
                    targets_in_degree, "target_name", linked_source
                )

                if target_detail == None:
                    result = False
                    messages.append(
                        f'Target {linked_source} in Observation {obs["obset_id"]} is'
                        " not found in proposal target"
                    )
                else:
                    if obs["array"] == "MID":
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

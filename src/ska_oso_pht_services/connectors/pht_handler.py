from datetime import datetime

import astropy.units as u
from astropy.coordinates import Angle


def transform_update_proposal(data: dict) -> dict:
    """
    Transforms and updates a given data dictionary with specific operations.

    The function performs the following transformations:
    - Sets the 'proposal_id' field to "12345" if the original 'proposal_id' is "new".
    - Adds or modifies date-related metadata.
    - Rounds 'right_ascension' and 'declination' in 'targets' to 3 decimal places.
    - Changes the units of 'right_ascension' and 'declination' to degrees.

    Parameters:
    data (dict): A dictionary containing various fields, including 'proposal_id',
                 'submitted_by', 'submitted_on', and nested 'proposal_info'
                 which includes 'investigators' and 'targets'.

    Returns:
    dict: The transformed and updated data dictionary.
    """
    # Transforming targets
    for target in data.get("proposal_info", {}).get("targets", []):
        for key, unit in [("right_ascension", u.hour), ("declination", u.deg)]:
            target[key] = round(Angle(target[key], unit=unit).degree, 3)
            target[f"{key}_unit"] = "deg"

    # Constructing and returning the updated data
    if data["submitted_by"] != "":
        # Constructing and returning the updated data
        return {
            "prsl_id": data["prsl_id"] if data["prsl_id"] != "new" else "12345",
            "submitted_by": data["submitted_by"],
            "submitted_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "submitted" if data["submitted_on"] else "draft",
            "investigators": [
                user["investigator_id"]
                for user in data.get("proposal_info", {}).get("investigators", [])
            ],
            "proposal_info": data.get("proposal_info", {}),
            "metadata": {
                "created_by": "next",
                "last_modified_by": "next",
                "created_date": "2022-10-03T01:23:45.678Z",
                "last_modified_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": 1,
            },
        }
    else:
        return {
            "prsl_id": data["prsl_id"],
            "status": "submitted" if data["submitted_on"] else "draft",
            "investigators": [
                user["investigator_id"]
                for user in data.get("proposal_info", {}).get("investigators", [])
            ],
            "proposal_info": data.get("proposal_info", {}),
            "metadata": {
                "created_by": "next",
                "last_modified_by": "next",
                "created_date": "2022-10-03T01:23:45.678Z",
                "last_modified_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": 1,
            },
        }


def transform_create_proposal(data: dict) -> dict:
    """
    Transforms and updates a given data dictionary with specific operations.

    The function performs the following transformations:
    - Sets the 'proposal_id' field to "new" .
    - Adds or modifies date-related metadata.

    Parameters:
    data (dict): A dictionary containing various fields, including 'proposal_id',
                 'submitted_by', 'submitted_on', and nested 'proposal_info'
                 which includes 'investigators' and 'targets'.

    Returns:
    dict: The updated data dictionary.
    """
    return {
        "status": "draft",
        "proposal_info": data.get("proposal_info", {}),
        "metadata": {
            "created_by": "next",
            "last_modified_by": "next",
            "created_date": "2022-10-03T01:23:45.678Z",
            "last_modified_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": 1,
        },
    }


# def upload_pdf_s3(file: str) -> dict:
# return "test"

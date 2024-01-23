from datetime import datetime
from astropy.coordinates import Angle
import astropy.units as u




def transform_update_proposal(data: object):
    updated_data = {"proposal_id": "prls-12321-94448" if data['proposal_id'] != "new" else data['proposal_id'],
    "submitted_by": data['submitted_by'],
    "submitted_date": data['submitted_on'],
    "status": "submitted" if data['submitted_on'] != "" else "draft",
    "investigators" : [user['investigator_id'] for user in data['proposal_info']['investigators']]
    }
    for target in data["proposal_info"]["targets"]:
        target["right_ascension"] = round((Angle(target["right_ascension"], unit=u.hour)).degree, 3)
        target["declination"] = round((Angle(target["declination"],unit=u.deg)).degree, 3)
        target["right_ascension_unit"] = "deg"
        target["declination_unit"] = "deg"

    meta_data = {
        "created_by": "next",
        "last_updated_by": "next",
        "created_date": "2022-10-03T01:23:45.678Z",
        "last_updated_on":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "version":1
    }
    return { **updated_data, **{"meta_data": meta_data, "proposal_info": data['proposal_info']}}
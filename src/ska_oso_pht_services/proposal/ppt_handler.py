import six
from ska_ser_skuid.client import SkuidClient
from datetime import datetime
from pydantic import BaseModel
import json
from datetime import date
import json
import psycopg2
import uuid
from models import ProposalDefinition, deserialize_to_dict, serialize_to_model, PayLoad

with open("../constants/data.json", "r") as file:
    data = json.load(file)


def update_meta_data(fulldata):
    data = fulldata["meta_data"]
    if all(
        key in data and data[key] is None
        for key in ["last_updated_date", "submitted_date"]
    ):
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_meta_data = {
            "skauuid": f'{"ppt-"}{uuid.uuid4()}',
            "created_date": created_date,
        }
    if data["created_date"] is not None and data["submitted_date"] is None:
        updated_meta_data = {
            "skauuid": f'{"ppt-"}{uuid.uuid4()}',
            "last_updated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    if data["status"] == "submitted":
        updated_meta_data = {
            "skauuid": f'{"ppt-"}{uuid.uuid4()}',
            "submitted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    meta_data = {
        "skauuid": updated_meta_data["skauuid"],
        "created_by": data["created_by"],
        "submitted_by": data["submitted_by"],
        "updated_by": data["updated_by"],
        "status": "submitted",
        "last_updated_date": "2023-12-21 19:32:00",
        "created_date": "2023-12-21 19:32:00",
    }
    return {**meta_data, **updated_meta_data}


def store_proposal(proposal, model):
    meta_data = update_meta_data(proposal)
    prep_data = {**{"meta_data": meta_data}, **{"proposal": proposal["proposal"]}}
    pop = serialize_to_model(proposal, model)
    return None


# print(store_proposal(data, ProposalDefinition))
def extract_users(proposal):
    data = proposal["proposal"]["investigator"]
    team = {i["investigator_id"] for i in data}
    return team


def extract_stored_proposal():
    data = deserialize_to_dict()
    return None


def create_payload_insert(proposal):
    payload = {
        "meta_data": update_meta_data(proposal),
        "investigator": extract_users(proposal),
        "proposal": proposal["proposal"],
    }
    pop = serialize_to_model(payload, PayLoad)
    return pop



from datetime import datetime
import json
import base64

def transform_save_proposal(data: object):
    updated_data = {"proposal_id": "project_123333/2024" if data['proposal_id'] == "" else data['proposal_id'],
    "submitted_by": data['submitted_by'],
    "submitted_date": data['submitted_on'],
    "status": "submitted" if data['submitted_on'] != "" else "draft"

    # submitted on empty -> it was a save proposal
  
    }
    return { **updated_data, **{"proposal": data['info']}}
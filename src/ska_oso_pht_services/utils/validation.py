import json
import os.path

from ska_oso_pdm.generated.models.proposal import Proposal
from ska_oso_pdm.openapi import CODEC as OPENAPI_CODEC


#TODO: use values from OSD after connection is ready

def load_string_from_file(filename):
    """
    Return a file from the current directory as a string
    """
    cwd, _ = os.path.split(__file__)
    path = os.path.join(cwd, filename)
    with open(path, "r", encoding="utf-8") as json_file:
        json_data = json_file.read()
        return json_data
    
def search_objects_by_key(objects, key, value):
    for obj in objects:
        if key in obj and obj[key] == value:
            return obj
    return None 

def validate_proposal(proposal_str) -> dict:
    """
    validate targets in a proposal

    Parameters:
    proposal_str (str): proposal
    
    Returns:
    dict: result of validation and message
    """
    
    lat_low = -26.82472208
    lat_mid = -30.712925
    min_ele = 15
    
    dec_min_low =  lat_low - 90 + min_ele
    dec_max_low = 90 - lat_low - min_ele
    
    dec_min_mid = lat_mid - 90 + min_ele
    dec_max_mid = 90 - lat_mid - min_ele
    
    result = True
    
    
    messages = []
    try:
        print('validate_proposal start try')
        # TODO: sample data not passing through CODEC
        # proposal = OPENAPI_CODEC.loads(Proposal, proposal_str)
        
        proposal = json.loads(proposal_str)
        
        # print('validate_proposal after CODEC')
        # print(proposal)
        # print(type(proposal))
        
        for obs in proposal['proposal_info']['observation_set']:
            print(obs)
            #case MID/LOW
            match obs['array']:
                case 'MID':
                    dec_min = dec_min_mid    
                    dec_max = dec_max_mid
                    pass
                case 'LOW':
                    dec_min = dec_min_low    
                    dec_max = dec_max_low
                    pass
                case _ :
                    raise(ValueError(f'array is not found in observation set {obs["obset_id"]}'))
            for linked_source in obs['linked_sources']:
                print(linked_source)
                target_detail = search_objects_by_key(proposal['proposal_info']['targets'], 'target_name', linked_source)
                
                if(target_detail == None):
                    raise(ValueError(f'target {linked_source} in observation {obs["obset_id"]} is not found in proposal target'))
                else:
                    print(f'obs:{obs} - target_detail:{target_detail}')
                    # convert everything to degree
                    # check values inside target_detail
                    # Determine if the declination is within range
                    print(target_detail)
    except (ValueError) as err:
        print(err)
        messages.append(str(err))
        return {
            "result": False,
            "validation_errors": messages}

    return {
        "result": result,
        "validation_errors": messages}


#-----------------------------------------For testing--------------------------------------------
SAMPLE_PROPOSAL_FOR_VALIDATE = load_string_from_file("sample_proposal_for_validation.json")

print(SAMPLE_PROPOSAL_FOR_VALIDATE)
print(type(SAMPLE_PROPOSAL_FOR_VALIDATE))
validate_proposal(SAMPLE_PROPOSAL_FOR_VALIDATE)
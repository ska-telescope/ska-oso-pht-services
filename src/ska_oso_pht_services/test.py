import json
from connectors.proposal_handler import transform_save_proposal
with open('./src/ska_oso_pht_services/constants/data.json', 'r') as file:

from connectors.proposal_handler import transform_save_proposal

with open(
    "./src/ska_oso_pht_services/constants/data.json", "r", encoding="utf-8"
) as file:
    # Parse the JSON data
    data_in = json.load(file)

top = transform_save_proposal(data_in)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(top, f, ensure_ascii=False, indent=4)

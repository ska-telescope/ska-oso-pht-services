import json
from connectors.proposal_handler import transform_save_proposal, decode_json_and_save_pdf
with open('./src/ska_oso_pht_services/constants/data.json', 'r') as file:
    # Parse the JSON data
    data_in = json.load(file)

top = transform_save_proposal(data_in)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(top, f, ensure_ascii=False, indent=4)

with open('./data.json', 'r') as file:
    # Parse the JSON data
    data_out = json.load(file)
json_data = data_out['pdf']

# Replace 'path/to/output_file.pdf' with your desired output file path
decode_json_and_save_pdf(json_data, './output_file.pdf')
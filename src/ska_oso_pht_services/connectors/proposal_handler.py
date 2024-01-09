from datetime import datetime
import json
import base64

def pdf_to_json_key_value(pdf_file_path):
    # Read the PDF file as binary data
    with open(pdf_file_path, 'rb') as pdf_file:
        binary_pdf = pdf_file.read()

    encoded_pdf = base64.b64encode(binary_pdf).decode('utf-8')
    # json_data = {json_key: encoded_pdf}
    # json_string = json.dumps(json_data, indent=4)
    return encoded_pdf


def decode_json_and_save_pdf(json_data, output_pdf_file_path):
    # Extract the Base64-encoded data from the JSON object
    encoded_pdf = json_data

    # Decode the Base64 data to binary
    binary_pdf = base64.b64decode(encoded_pdf)

    # Write the binary data to a new PDF file
    with open(output_pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(binary_pdf)



def transform_save_proposal(data: object):
    updated_data = {"proposal_id": "project_123333/2024" if data['proposal_id'] == "" else data['proposal_id'],
    "submitted_by": data['submitted_by'],
    "submitted_date": data['submitted_on'],
    "cycle": "SKAO_123333/2024" if data['cycle'] == "" else data['cycle'],
    "status": "submitted" if data['submitted_on'] != "" else "draft"
  
    }
    meta_data = {
        "created_by": "next",
        "last_updated_by": "next",
        "created_date": "2022-10-03T01:23:45.678Z",
        "last_updated_on":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    pdf =pdf_to_json_key_value('./test.pdf')
    return {**{"pdf": pdf},  **updated_data, **{"meta_data": meta_data, "proposal": data['proposal']}}
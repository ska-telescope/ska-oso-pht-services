import boto3
from botocore.exceptions import NoCredentialsError

def upload_pdf_to_s3_and_get_details(aws_access_key, aws_secret_key, bucket_name, local_file_path, s3_file_key):
    """
    Uploads a PDF file to an Amazon S3 bucket and returns its details.

    Parameters:
    aws_access_key (str): AWS access key ID.
    aws_secret_key (str): AWS secret access key.
    bucket_name (str): Name of the S3 bucket.
    local_file_path (str): Path to the local PDF file.
    s3_file_key (str): Desired key (path) for the file in the S3 bucket.

    Returns:
    dict: A dictionary containing details of the uploaded file.
    """
    try:
        # Initialize the S3 client
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

        # Upload the file
        s3_client.upload_file(local_file_path, bucket_name, s3_file_key)
        print(f"File '{local_file_path}' uploaded to '{s3_file_key}' in bucket '{bucket_name}'.")

        # Get the file details
        response = s3_client.head_object(Bucket=bucket_name, Key=s3_file_key)

        # Construct and return the file details
        file_details = {
            'File Key': s3_file_key,
            'File Size': response['ContentLength'],
            'Content Type': response['ContentType'],
            'Last Modified': response['LastModified']
        }
        return file_details

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(e)
        return None

# Example usage
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
bucket_name = 'YOUR_BUCKET_NAME'
local_file_path = 'PATH_TO_YOUR_LOCAL_PDF_FILE'
s3_file_key = 'DESIRED_S3_FILE_KEY.pdf'

file_details = upload_pdf_to_s3_and_get_details(aws_access_key, aws_secret_key, bucket_name, local_file_path, s3_file_key)
if file_details:
    print(file_details)

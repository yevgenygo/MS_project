import argparse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Upload and copy blobs between two Azure storage accounts.")
parser.add_argument('--source_sas_url', type=str, required=True, help='SAS URL of the source storage account')
parser.add_argument('--destination_sas_url', type=str, required=True, help='SAS URL of the destination storage account')
parser.add_argument('--source_container', type=str, required=True, help='Source container name')
parser.add_argument('--destination_container', type=str, required=True, help='Destination container name')

args = parser.parse_args()

# Initialize BlobServiceClients
source_blob_service_client = BlobServiceClient(account_url=args.source_sas_url)
destination_blob_service_client = BlobServiceClient(account_url=args.destination_sas_url)

# Function to create container if it doesn't exist
def create_container_if_not_exists(service_client, container_name):
    try:
        service_client.create_container(container_name)
        print(f"Container '{container_name}' created.")
    except Exception:
        print(f"Container '{container_name}' already exists.")

# Create containers in both storage accounts
create_container_if_not_exists(source_blob_service_client, args.source_container)
create_container_if_not_exists(destination_blob_service_client, args.destination_container)

# Upload 100 blobs to the source storage account
for i in range(1, 101):
    blob_name = f"sample_blob_{i}.txt"
    blob_content = f"This is blob number {i}"
    blob_client = source_blob_service_client.get_blob_client(container=args.source_container, blob=blob_name)
    blob_client.upload_blob(blob_content, overwrite=True)
    print(f"Uploaded blob: {blob_name}")

# Copy blobs from source storage account to destination storage account
for i in range(1, 101):
    blob_name = f"sample_blob_{i}.txt"
    source_blob_url = f"{args.source_sas_url}/{args.source_container}/{blob_name}?{args.source_sas_url.split('?')[1]}"
    destination_blob_client = destination_blob_service_client.get_blob_client(container=args.destination_container, blob=blob_name)
    destination_blob_client.start_copy_from_url(source_blob_url)
    print(f"Copied blob {blob_name} from storage account A to B.")

print("All blobs uploaded and copied successfully!")

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# SAS URLs for both storage accounts
source_sas_url = "https://mystorageaccounta12345.blob.core.windows.net/?sv=2022-11-02&ss=b&srt=sco&sp=rwdlactfx&se=2025-03-22T20:13:47Z&st=2025-02-22T12:13:47Z&spr=https&sig=99pmeFRIB46%2FS3iwxnAVnwuMScqUTj8mS0xqdn4nOeM%3D"
destination_sas_url = "https://mystorageaccountb12345.blob.core.windows.net/?sv=2022-11-02&ss=b&srt=sco&sp=rwdlactfx&se=2025-03-22T20:16:08Z&st=2025-02-22T12:16:08Z&spr=https&sig=5utIWdLUfcmtu5TQtsQbNbQAszH4M05EGKjyJqow5Sg%3D"

# Initialize BlobServiceClient with SAS tokens
source_blob_service_client = BlobServiceClient(account_url=source_sas_url)
destination_blob_service_client = BlobServiceClient(account_url=destination_sas_url)

# Container names
source_container_name = "container-a"
destination_container_name = "container-b"

# Function to create container if it doesn't exist
def create_container_if_not_exists(service_client, container_name):
    try:
        service_client.create_container(container_name)
        print(f"Container '{container_name}' created.")
    except Exception:
        print(f"Container '{container_name}' already exists.")

# Create containers in both storage accounts
create_container_if_not_exists(source_blob_service_client, source_container_name)
create_container_if_not_exists(destination_blob_service_client, destination_container_name)

# Upload 100 blobs to the source storage account
for i in range(1, 101):
    blob_name = f"sample_blob_{i}.txt"
    blob_content = f"This is blob number {i}"
    blob_client = source_blob_service_client.get_blob_client(container=source_container_name, blob=blob_name)
    blob_client.upload_blob(blob_content, overwrite=True)
    print(f"Uploaded blob: {blob_name}")

# Copy blobs from source storage account to destination storage account
for i in range(1, 101):
    blob_name = f"sample_blob_{i}.txt"
    source_blob_url = f"https://mystorageaccounta12345.blob.core.windows.net/{source_container_name}/{blob_name}?{source_sas_url.split('?')[1]}"
    destination_blob_client = destination_blob_service_client.get_blob_client(container=destination_container_name, blob=blob_name)
    destination_blob_client.start_copy_from_url(source_blob_url)
    print(f"Copied blob {blob_name} from storage account A to B.")

print("All blobs uploaded and copied successfully!")

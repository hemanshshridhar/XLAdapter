from azure.storage.blob import BlobServiceClient
import os
import urllib
from concurrent.futures import ThreadPoolExecutor
from llmadapter.constants import (
    AzureConstants
)


class BlobStorageUtil:
    def __init__(self):
        self.blob_service_client, self.blob_container_client = self.create_clients()

    def download_files_parallel(self, blob_paths, local_download_paths, show_progress=True, max_workers=16):
        result_blob_to_local_dict = {}
        def download_file(blob_path, local_path):
            try:
                blob_client = self.blob_container_client.get_blob_client(blob=blob_path)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, "wb") as download_file:
                    download_file.write(blob_client.download_blob(timeout=300).readall())

                if show_progress:
                    print(f"Downloaded {blob_path} to {local_path}")

                result_blob_to_local_dict[blob_path] = local_path
            except Exception as e:
                print(f"Failed to download {blob_path}: {e}")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for blob_path, local_path in zip(blob_paths, local_download_paths):
                executor.submit(download_file, blob_path, local_path)

        return result_blob_to_local_dict
    
    def create_clients(self):
        parsed_url = urllib.parse.urlparse(AzureConstants.LLM_SAS_URL)
        CONTAINER_NAME = parsed_url.path.strip('/')
        account_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        credential = parsed_url.query
        blob_service_client = BlobServiceClient(
            account_url=account_url, credential=credential
        )
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        return blob_service_client, container_client
    
import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GCP_CREDENTIALS")

class GCStorage:
    def __init__(self):
        self.storage_client = storage. Client()
        self.bucket_name = 'kumsia-storage'

    def upload_file(self, file):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        file_path = file.filename
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file, content_type='image/jpeg')
        return f'https://storage.cloud.google.com/{self.bucket_name}/{file_path}'
import logging

from storage import StorageInterface
from storage.env import *
from obs import ObsClient, PutObjectHeader


class StorageObs(StorageInterface):

    def download_file(self, file_path, key):
        pass

    def download_directory(self, key, local_target_directory):
        pass

    def generate_signed_url(self, key, expiration=600):
        pass

    def generate_upload_credentials(self, key, expiration=3600):
        pass

    def __init__(self, cfgs=None):
        if cfgs is None:
            cfgs = {}
        self._bucket = STORAGE_BUCKET
        self._client = ObsClient(
            access_key_id=OBS_ACCESS_KEY_ID,
            secret_access_key=OBS_SECRET_ACCESS_KEY,
            server=OBS_SERVER
        )

    def write_bytes(self, content_bytes, key):
        self.write_string(content_bytes, key)

    def write_string(self, content_string, key):
        try:
            self._client.putContent(self._bucket, key, content=content_string)
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)

    def upload_file(self, file_path, key):
        headers = PutObjectHeader()
        headers.contentType = 'text/plain'
        self._client.putFile(self._bucket, key, file_path, metadata={}, headers=headers)

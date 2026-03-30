import json
from datetime import datetime as dt

from repositories import S3Repository


class StorageService:
    def __init__(self, repo: S3Repository):
        """Service to store/read data."""
        self._repo = repo

    def get(self, key):
        data = self._repo.get_body(key)
        return json.loads(data)

    def save_or_update(self, key, data):
        return self._repo.save_or_update_file(key, json.dumps(data))

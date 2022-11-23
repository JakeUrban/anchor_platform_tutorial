from os import environ
import requests


class AnchorPlatformClient:
    def __init__(self):
        self._session = None
        self._base_url = environ.get("ANCHOR_PLATFORM_BASE_URL")

    def __enter__(self) -> "AnchorPlatformClient":
        if not self._session:
            self._session = requests.Session()
        return self

    def __exit__(self, *args) -> bool:
        self._session.close()
        return False

    def get_transaction(self, tid: str) -> dict:
        response = self._session.get(f"{self._base_url}/transactions/{tid}")
        return response.json()

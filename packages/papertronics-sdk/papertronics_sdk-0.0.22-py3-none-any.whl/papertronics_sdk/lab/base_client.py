import logging

import httpx

from .exceptions import StatusException

logger = logging.getLogger(__name__)


def http_request(func):
    def wrap(self, url, **kwargs):
        if self.token is None:
            raise Exception("Client is not Authenticated")

        print(self)
        print(url)

        url = f"{self.url}{url}"
        if kwargs.get("include_token", True):
            kwargs["headers"] = kwargs.get("headers", {})
            kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
        response = func(self, url, **kwargs)
        logger.debug(f"{func.__name__} {url} {response.status_code}")
        if response.status_code != 200:
            raise StatusException.from_response(response)
        return response

    return wrap

class BaseClient:

    def __init__(self, url, token=None):
        self.url = url
        self.token = token
        try:
            response = self.get(f"")
            if response.status_code != 200:
                raise Exception(response.status_code)
        except Exception as e:
            raise Exception(f"could not connect to {url}: {e}")

    @http_request
    def get(self, url, **kwargs):
        return httpx.get(url, **kwargs)

    @http_request
    def post(self, url, **kwargs):
        return httpx.post(url, **kwargs)

    @http_request
    def delete(self, url, **kwargs):
        return httpx.delete(url, **kwargs)


import logging
import time
import uuid
from typing import Optional, List, Union

import httpx

from .models.database import DeviceModel, UserModel, ProtocolModel, ExperimentModel, ExperimentStatus
from .models.cloud_models import SaveProtocolRequest, ProtocolTestResponse, ExperimentStartRequest, \
    ExperimentEditRequest
from .exceptions import StatusException

logger = logging.getLogger(__name__)


class BaseClient:

    def __init__(self, url, token=None):
        self.url = url
        self.token = token

    def http_request(self, func):
        def wrap(path, **kwargs):
            if self.token is None:
                raise Exception("Client is not Authenticated")

            url = f"{self.url}{path}"
            if kwargs.get("include_token", True):
                kwargs["headers"] = kwargs.get("headers", {})
                kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
            response = func(url, **kwargs)
            logger.debug(f"{func.__name__} {url} {response.status_code}")
            if response.status_code != 200:
                raise StatusException.from_response(response)
            return response

        return wrap

    @http_request
    def get(self, url, **kwargs):
        return httpx.get(url, **kwargs)

    @http_request
    def post(self, url, **kwargs):
        return httpx.post(url, **kwargs)

    @http_request
    def delete(self, url, **kwargs):
        return httpx.delete(url, **kwargs)


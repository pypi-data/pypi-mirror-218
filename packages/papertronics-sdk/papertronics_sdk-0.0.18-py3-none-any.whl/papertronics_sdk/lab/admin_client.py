import uuid
from typing import Optional, Union, List

from .models.database import DeviceModel, DeviceLinkModel, DeviceStatisticModel, ProtocolModel, ProtocolLinkModel, \
    UserModel
from .models.admin_cloud_models import DeviceRequest, UserRequest
from base_client import BaseClient


class AdminLabClient(BaseClient):

    def __init__(self, url, token):
        super().__init__(url, token)

    async def login_user(self, user_id: uuid.UUID) -> str:
        response = self.post(f"{self.url}/admin/auth/token?user_id={user_id}",
                             headers={"Authorization": f"Bearer {self.token}"})
        return response.json().get("access_token")

    async def get_users(self, user_id: Optional[uuid.UUID] = None) -> Union[List[UserModel], UserModel]:
        response = self.get(f"{self.url}/admin/user?user_id={user_id}",
                            headers={"Authorization": f"Bearer {self.token}"})
        response_dict = response.json()
        if type(response_dict) == list:
            return [UserModel.parse_obj(r) for r in response_dict]
        else:
            return UserModel.parse_obj(response_dict)

    async def add_user(self, add_user_request: UserRequest) -> UserModel:
        response = self.post(f"{self.url}/admin/user", json=add_user_request.dict(),
                             headers={"Authorization": f"Bearer {self.token}"})
        return UserModel.parse_obj(response.json())

    async def delete_user(self, user_id: uuid.UUID):
        self.delete(f"{self.url}/admin/user?user_id={user_id}",
                    headers={"Authorization": f"Bearer {self.token}"})

    async def update_user(self, user_id: uuid.UUID, add_user_request: UserRequest) -> UserModel:
        response = self.post(f"{self.url}/admin/user/update?user_id={user_id}", json=add_user_request.dict(),
                             headers={"Authorization": f"Bearer {self.token}"})
        return UserModel.parse_obj(response.json())

    async def get_protocol(self, protocol_id: Optional[uuid.UUID] = None) -> Union[ProtocolModel, List[ProtocolModel]]:
        response = self.get(f"{self.url}/admin/protocol?protocol_id={protocol_id}",
                            headers={"Authorization": f"Bearer {self.token}"})
        response_dict = response.json()
        if type(response_dict) == list:
            return [ProtocolModel.parse_obj(r) for r in response_dict]
        else:
            return ProtocolModel.parse_obj(response_dict)

    async def link_protocol(self, protocol_id: uuid.UUID, user_id: uuid.UUID) -> ProtocolLinkModel:
        response = self.post(f"{self.url}/admin/protocol/link?protocol_id={protocol_id}&user_id={user_id}",
                             headers={"Authorization": f"Bearer {self.token}"})
        return ProtocolLinkModel.parse_obj(response.json())

    async def remove_link_protocol(self, protocol_link_id: uuid.UUID):
        self.delete(f"{self.url}/admin/protocol/link?protocol_link_id={protocol_link_id}",
                    headers={"Authorization": f"Bearer {self.token}"})

    async def get_devices(self, device_id: Optional[uuid.UUID] = None) -> Union[List[DeviceModel], DeviceModel]:
        response = self.get(f"{self.url}/admin/device?device_id={device_id}",
                            headers={"Authorization": f"Bearer {self.token}"})
        response_dict = response.json()
        if type(response_dict) == list:
            return [DeviceModel.parse_obj(r) for r in response_dict]
        else:
            return DeviceModel.parse_obj(response_dict)

    async def add_device(self, add_device_request: DeviceRequest) -> DeviceModel:
        response = self.post(f"{self.url}/admin/device", json=add_device_request.dict(),
                             headers={"Authorization": f"Bearer {self.token}"})
        return DeviceModel.parse_obj(response.json())

    async def delete_device(self, device_id: uuid.UUID):
        self.delete(f"{self.url}/admin/device?device_id={device_id}",
                    headers={"Authorization": f"Bearer {self.token}"})

    async def update_device(self, device_id: uuid.UUID, add_device_request: DeviceRequest) -> DeviceModel:
        response = self.post(f"{self.url}/admin/device/update?device_id={device_id}", json=add_device_request.dict(),
                             headers={"Authorization": f"Bearer {self.token}"})
        return DeviceModel.parse_obj(response.json())

    async def link_device(self, device_id: uuid.UUID, user_id: uuid.UUID) -> DeviceLinkModel:
        response = self.post(f"{self.url}/admin/device/link?device_id={device_id}&user_id={user_id}",
                             headers={"Authorization": f"Bearer {self.token}"})
        return DeviceLinkModel.parse_obj(response.json())

    async def remove_link_device(self, device_link_id: uuid.UUID):
        self.delete(f"{self.url}/admin/device/link?device_link_id={device_link_id}",
                    headers={"Authorization": f"Bearer {self.token}"})

    async def get_device_statistics(self, device_id: Optional[uuid.UUID] = None) -> List[DeviceStatisticModel]:
        response = self.get(f"{self.url}/admin/device/statistic?device_id={device_id}",
                            headers={"Authorization": f"Bearer {self.token}"})
        return [DeviceStatisticModel.parse_obj(r) for r in response.json()]

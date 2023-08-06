import time
import uuid
from typing import Optional, List, Union

from .models.database import DeviceModel, UserModel, ProtocolModel, ExperimentModel, ExperimentStatus
from .models.cloud_models import SaveProtocolRequest, ProtocolTestResponse, ExperimentStartRequest, \
    ExperimentEditRequest
from .base_client import BaseClient


class UserLabClient(BaseClient):

    def authenticate(self, email, password):
        response = self.post(f"{self.url}/auth/token", data=dict(username=email, password=password))
        self.token = response.json().get("access_token")
        return self.token

    def authenticate_device(self, device_id: uuid.UUID):
        response = self.post(f"{self.url}/auth/device?device_id={device_id}",
                             headers={"Authorization": f"Bearer {self.token}"})
        self.token = response.json().get("access_token")
        return self.token

    def download_data(self):
        return "not implemented"

    async def download_image(self,
                             blob_name: str):
        return "not implemented"

    async def get_device_info(self) -> DeviceModel:
        response = self.get(f"{self.url}/device",
                            headers={"Authorization": f"Bearer {self.token}"})
        return DeviceModel.parse_obj(response.json())

    async def get_devices(self) -> List[DeviceModel]:
        response = self.get(f"{self.url}/device/all",
                            headers={"Authorization": f"Bearer {self.token}"})
        return [DeviceModel.parse_obj(r) for r in response.json()]

    async def get_user_info(self) -> UserModel:
        response = self.get(f"{self.url}/user",
                            headers={"Authorization": f"Bearer {self.token}"})
        return UserModel.parse_obj(response.json())

    def store_protocol(self, protocol_request: SaveProtocolRequest) -> ProtocolModel:
        response = self.post(f"{self.url}/protocol",
                             headers={"Authorization": f"Bearer {self.token}"},
                             json=protocol_request.dict())
        return ProtocolModel.parse_obj(response.json())

    def build_protocol(self,
                       protocol_request: SaveProtocolRequest,
                       duration: int,
                       interval: int,
                       flash: bool = True,
                       start_delay: int = 0) -> ProtocolModel:
        response = self.post(
            f"{self.url}/protocol/build?duration={duration}&interval={interval}&flash={flash}&start_delay={start_delay}",
            headers={"Authorization": f"Bearer {self.token}"},
            json=protocol_request.dict())
        return ProtocolModel.parse_obj(response.json())

    def get_protocol(self,
                     protocol_id: Optional[uuid.UUID] = None,
                     protocol_test_type: Optional[str] = None,
                     page_size: Optional[int] = None,
                     page: Optional[int] = None,
                     valid: Optional[bool] = True) -> Union[ProtocolModel, List[ProtocolModel]]:
        response = self.get(f"{self.url}/protocol",
                            headers={"Authorization": f"Bearer {self.token}"},
                            params=dict(protocol_id=protocol_id,
                                        protocol_test_type=protocol_test_type,
                                        page_size=page_size,
                                        page=page,
                                        valid=valid))
        if type(response.json()) == list:
            return [ProtocolModel.parse_obj(r) for r in response.json()]
        else:
            return ProtocolModel.parse_obj(response.json())

    def count_protocol(self,
                       protocol_test_type: Optional[str] = None,
                       valid: Optional[bool] = True) -> int:
        response = self.get(f"{self.url}/protocol/count",
                            headers={"Authorization": f"Bearer {self.token}"},
                            params=dict(protocol_test_type=protocol_test_type,
                                        valid=valid))
        return int(response.text)

    def get_protocol_test_def(self, protocol_id: uuid.UUID) -> Union[ProtocolTestResponse, str]:
        response = self.get(f"{self.url}/protocol/test?protocol_id={protocol_id}",
                            headers={"Authorization": f"Bearer {self.token}"})
        if type(response.json()) == str:
            return response.json()
        else:
            return ProtocolTestResponse.parse_obj(response.json())

    def invalidate_protocol(self, protocol_id: uuid.UUID) -> ProtocolModel:
        response = self.delete(f"{self.url}/protocol?protocol_id={protocol_id}",
                               headers={"Authorization": f"Bearer {self.token}"})
        return ProtocolModel.parse_obj(response.json())

    async def start_experiment(self, request: ExperimentStartRequest) -> ExperimentModel:
        response = self.post(f"{self.url}/experiment/start",
                             headers={"Authorization": f"Bearer {self.token}"},
                             json=request.dict())
        return ExperimentModel.parse_obj(response.json())

    def cancel_experiment(self,
                          experiment_id: uuid.UUID):
        self.post(f"{self.url}/experiment/cancel",
                  headers={"Authorization": f"Bearer {self.token}"},
                  json=dict(experiment_id=experiment_id))

    def get_experiments(self,
                        experiment_id: Optional[List[uuid.UUID]] = None,
                        device_id: Optional[uuid.UUID] = None,
                        order_by: str = "start_time",
                        ascending_order: bool = False,
                        page_size: Optional[int] = None,
                        page: Optional[int] = None,
                        valid: Optional[bool] = None,
                        first=True) -> Union[List[ExperimentModel], ExperimentModel]:
        response = self.get(f"{self.url}/experiment",
                            headers={"Authorization": f"Bearer {self.token}"},
                            params=dict(experiment_id=experiment_id,
                                        device_id=device_id,
                                        order_by=order_by,
                                        ascending_order=ascending_order,
                                        page_size=page_size,
                                        page=page,
                                        valid=valid))
        if first:
            return ExperimentModel.parse_obj(response.json()[0])
        else:
            return [ExperimentModel.parse_obj(r) for r in response.json()]

    def count_experiments(self,
                          valid: Optional[bool] = None,
                          device_id: Optional[uuid.UUID] = None) -> int:
        response = self.get(f"{self.url}/experiment/count",
                            headers={"Authorization": f"Bearer {self.token}"},
                            params=dict(device_id=device_id,
                                        valid=valid))
        return int(response.text)

    def edit_experiment_by_id(self,
                              experiment_id: uuid.UUID,
                              experiment_edit_request: ExperimentEditRequest):
        response = self.post(f"{self.url}/experiment/edit?experiment_id={experiment_id}",
                             headers={"Authorization": f"Bearer {self.token}"},
                             json=experiment_edit_request.dict())
        return ExperimentModel.parse_obj(response.json())

    def delete_experiment_by_id(self,
                                experiment_id: uuid.UUID):
        self.delete(f"{self.url}/experiment?experiment_id={experiment_id}",
                    headers={"Authorization": f"Bearer {self.token}"})

    def perform_experiment(self, request: ExperimentStartRequest, timeout=120):
        response = self.post(f"{self.url}/experiment/start",
                             headers={"Authorization": f"Bearer {self.token}"},
                             json=request.dict())
        experiment = ExperimentModel.parse_obj(response.json())

        sleep_counter = 0
        images_captured = 0

        while experiment.status == ExperimentStatus.PENDING:
            time.sleep(1)
            sleep_counter += 1
            if sleep_counter > timeout:
                raise TimeoutError("Experiment timed out. Experiment status is still PENDING.")
            experiment = self.get_experiments(experiment_id=[experiment.id], first=True)

        while not (experiment.status == ExperimentStatus.FINISHED or
                   experiment.status == ExperimentStatus.FAILED or
                   experiment.status == ExperimentStatus.CANCELLED):
            time.sleep(1)
            experiment = self.get_experiments(experiment_id=[experiment.id], first=True)
            if len(experiment.image_extracts) > images_captured:
                images_captured = len(experiment.image_extracts)
                yield experiment

        yield experiment

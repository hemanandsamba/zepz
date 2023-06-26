from typing import Optional
from uuid import UUID

from zepz.mobile import IPAddress, Device
from zepz.common import UserInformation

list_of_tables = [
    "user_table",
    "recipient_table",
    "allowed_ip_table",
    "blocked_ip_table",
    "ip_risk_score_table",
    "allowed_device_table",
    "blocked_device_table",
    "send_country_policy",
    "receive_country_policy",
]


class ZeppsDB:
    def __init__(self, name):
        self._name = name

    def connect(self):
        pass

    def get_user_info(self, user_id: int) -> Optional[UserInformation]:
        pass

    def add_user_info(self, user_info: UserInformation) -> int:
        pass

    def is_ip_allowed(self, ip_address: str):
        pass

    def add_ip_address_risk_score(self, ip_address: IPAddress, risk_score: int):
        pass

    def add_allowed_device(self, device: Device):
        pass

    def add_blocked_device(self, device: Device):
        pass

    def is_device_allowed(self, device_id: UUID):
        pass

    def is_device_blocked(self, device_id: UUID):
        pass

    def push_verification_file(self, user_id: int, image_file: str) -> int:
        pass

    def push_selfie(self, user_id: int, id_file: str) -> int:
        pass

    def get_country_policies(self, country: str):
        pass

    def get_corridor_policy(self, send_country: str, receive_country: str):
        pass

    def close(self):
        pass

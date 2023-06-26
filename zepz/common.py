import enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class Required_ID(enum.Enum):
    # just a simple electronic verification with a 3rd party
    SIMPLE_VERIFICATION = 1

    ID_VERIFICATION = 2  # ID verification (user submitted ID), assumes
    # that simple verification has already happened or
    # wouldn't be sufficient

    SELFIE_MATCH = 3  # Implies that ID verification and
    # simple verification have happened or wouldn't be
    # sufficient


def get_required_ids(required_id: Required_ID) -> dict:
    ids_req = {
        Required_ID.SIMPLE_VERIFICATION.name: True,
        Required_ID.ID_VERIFICATION.name: False,
        Required_ID.SELFIE_MATCH.name: False,
    }

    if Required_ID.ID_VERIFICATION == required_id:
        ids_req[Required_ID.ID_VERIFICATION.name] = True

    else:
        ids_req[Required_ID.ID_VERIFICATION.name] = True
        ids_req[Required_ID.ID_VERIFICATION.name] = True

    return ids_req


def get_minimum_required_policy(required_id_policies: List[Required_ID]) -> Required_ID:
    if Required_ID.SELFIE_MATCH in required_id_policies:
        id_req = Required_ID.SELFIE_MATCH
    elif Required_ID.ID_VERIFICATION in required_id_policies:
        id_req = Required_ID.ID_VERIFICATION
    else:
        id_req = Required_ID.SELFIE_MATCH

    return id_req


class SimpleVerification:
    def __init__(
        self,
        user_id: Optional[int],
        first_name: Optional[str],
        last_name: Optional[str],
        address: Optional[str],
        email_id: Optional[str],
        middle_name: Optional[str] = "",
    ):
        self._user_id = user_id
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name
        self._address = address
        self._email_id = email_id

    def all_info_present(self) -> bool:
        if not self._user_id or not self._first_name or not self._last_name or not self._address:
            return False
        else:
            return True


class UserInformation:
    user_id: int
    simple_verification: SimpleVerification
    send_country: Optional[str] = ("",)
    receive_country: Optional[str] = ("",)
    # Identifier on DB that has the govt ID image
    verification_id: Optional[int] = None
    # Identifier on DB that has the selfie image
    selfie_picture_id: Optional[int] = None
    ip_address: Optional[str] = None
    device_uuid: Optional[UUID] = None
    transaction_count: int = None
    when_created: datetime = None


def get_country(address: str) -> str:
    pass

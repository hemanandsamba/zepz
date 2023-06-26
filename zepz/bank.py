from typing import Optional
from tkinter import Tk
from datetime import datetime

from zepz.common import get_required_ids, UserInformation, get_country
from zepz.transaction import Transaction
from zepz.risk import (
    risk_id_requirements,
    Required_ID,
    RiskError,
    RiskCategory,
    get_risk_category,
    get_user_risk_info,
    review_user_risk,
)
from zepz.mobile import (
    get_latest_device_id,
    get_latest_used_ip_address,
    prompt_user_simple_verification,
    prompt_user_drivers_license,
    prompt_user_selfie_pic,
)
from zepz.database import ZeppsDB

# we don't want a full GUI, so keep the root window from appearing
Tk().withdraw()


def add_user(user_id: int, transaction: Optional[Transaction]):
    zepps_db = ZeppsDB(name="ZeppsDB")
    zepps_db.connect()

    new_user = False
    user_info = zepps_db.get_user_info(user_id=user_id)

    if not user_info:
        user_info = UserInformation()
        user_info.user_id = user_id
        user_info.when_created = datetime.utcnow()
        new_user = True

    # The 3rd party info is the basic required ID
    if not user_info.simple_verification.all_info_present():
        user_info.simple_verification = prompt_user_simple_verification()

    if not user_info.send_country:
        user_info.send_country = get_country(user_info.simple_verification.ad)

    if not user_info.receive_country and transaction:
        user_info.receive_country = transaction.receive_country

    req_id = risk_id_requirements(user_id=user_info.user_id, transaction=transaction)
    required_id_forms = get_required_ids(required_id=req_id)

    # If Govt. issued ID is required, check and prompt if missing and push to DB
    if (
        required_id_forms[Required_ID.ID_VERIFICATION.name]
        or required_id_forms[Required_ID.SELFIE_MATCH.name]
    ):
        if not user_info.verification_id:
            dl_image_file = prompt_user_drivers_license()
            user_info.verification_id = zepps_db.push_verification_file(
                user_id=user_info.user_id, image_file=dl_image_file
            )

    # If selfie is required, check and prompt if missing and push to DB
    if required_id_forms[Required_ID.SELFIE_MATCH.name]:
        if not user_info.selfie_picture:
            selfie_file = prompt_user_selfie_pic()
            user_info.selfie_picture_id = zepps_db.push_selfie(
                user_id=user_info.user_id, id_file=selfie_file
            )

    user_risk_info = get_user_risk_info(user_id=user_info.user_id)

    latest_ip_address = get_latest_used_ip_address(user_id=user_info.user_id)
    if not zepps_db.is_ip_allowed(ip_address=latest_ip_address.ip):
        raise RiskError(
            f"The user {latest_ip_address.user_id} has IP address {latest_ip_address.ip} that's blocked"
        )
    zepps_db.add_ip_address_risk_score(
        ip_address=latest_ip_address, risk_score=user_risk_info.highest_ip_risk
    )

    latest_device_id = get_latest_device_id(user_id=user_info.user_id)
    if zepps_db.is_device_blocked(device_id=latest_device_id.device_id):
        raise RiskError(
            f"The user {latest_device_id.user_id} has has device ID {latest_device_id.device_id} that's blocked"
        )

    user_risk_category = get_risk_category(risk_score=user_risk_info.highest_ip_risk)

    if user_risk_category == RiskCategory.BLOCK:
        zepps_db.add_blocked_device(device=latest_device_id)
        raise RiskError(
            f"The user {user_risk_info.first_name} {user_risk_info.last_name} has risk value of {user_risk_info.highest_ip_risk} and categorized as {user_risk_category.name}"
        )
    elif user_risk_category == RiskCategory.NEEDS_REVIEW:
        if not review_user_risk(ip_address=user_info.ip_address, user_risk_info=user_risk_info):
            zepps_db.add_blocked_device(device=latest_device_id)
            raise RiskError(
                f"The user {user_risk_info.first_name} {user_risk_info.last_name} has been reviewed and categorized as blocked"
            )

    if not zepps_db.is_device_allowed(device_id=latest_device_id.device_id):
        zepps_db.add_allowed_device(device=latest_device_id)

    if new_user:
        zepps_db.add_user_info(user_info)

    zepps_db.close()

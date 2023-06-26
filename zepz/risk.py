import enum
from typing import Optional

from zepz.common import Required_ID, get_minimum_required_policy
from zepz.transaction import Transaction, get_id_policy

_MIN_RISK_SCORE = 0
_MAX_RISK_SCORE = 100


class RiskError(Exception):
    pass


class UserRiskInfo:
    first_name: str
    last_name: str
    highest_ip_risk: int
    has_id: bool


def _check_third_party(user_id: int) -> bool:
    return True


def get_user_risk_info(user_id: int) -> UserRiskInfo:
    # run the slackOps command /get_user_identify_info [USER_ID] and return the object
    return UserRiskInfo()


class RiskCategory(enum.Enum):
    CLEAR = 1
    NEEDS_REVIEW = 2
    BLOCK = 3


def get_risk_category(risk_score: int) -> RiskCategory:
    if risk_score < _MIN_RISK_SCORE or risk_score > _MAX_RISK_SCORE:
        raise RiskError(
            f"The risk score is not in the expected range: {_MIN_RISK_SCORE} - {_MAX_RISK_SCORE}"
        )

    if _MIN_RISK_SCORE <= risk_score < (_MIN_RISK_SCORE + _MAX_RISK_SCORE) / 3:
        risk_cat = RiskCategory.CLEAR
    elif (
        (_MIN_RISK_SCORE + _MAX_RISK_SCORE) / 3
        <= risk_score
        < (_MIN_RISK_SCORE + _MAX_RISK_SCORE) * 2 / 3
    ):
        risk_cat = RiskCategory.NEEDS_REVIEW
    else:
        risk_cat = RiskCategory.BLOCK

    return risk_cat


def risk_id_requirements(user_id: int, transaction: Optional[Transaction]) -> Required_ID:
    """
    Returns an enum with the minimum ID requirements from Risk.
    If the user has already satisfied those requirements, great,
    otherwise the user should be prompted to provide additional info
    :param user_id: unique ID of the user that risk uses
    to look up other information
    :param transaction: This check _can_ be associated with a transaction.

    If it is, risk uses the transaction info
    to inform the ID decision, otherwise it only uses
    other information.
    :return: Required_ID
    """
    transaction_based_req_id = Required_ID.SIMPLE_VERIFICATION

    if transaction:
        transaction_based_req_id = get_id_policy(
            transaction_count=transaction.transaction_count,
            send_country=transaction.send_country,
            receive_country=transaction.receive_country,
            amount=transaction.amount,
        )

    is_third_party_approved = _check_third_party(user_id=user_id)
    if is_third_party_approved:
        user_based_req_id = Required_ID.SIMPLE_VERIFICATION
    else:
        user_based_req_id = Required_ID.SELFIE_MATCH

    required_ids = [transaction_based_req_id, user_based_req_id]

    return get_minimum_required_policy(required_ids)


def review_user_risk(ip_address: str, user_risk_info: UserRiskInfo) -> bool:
    pass


if __name__ == "__main__":
    print(max(Required_ID.SIMPLE_VERIFICATION, Required_ID.ID_VERIFICATION))

from zepz.common import Required_ID

_MIN_SEND_THRESHOLD_ANY_TRANSACTION = 10
_MAX_SEND_THRESHOLD_ANY_TRANSACTION = 20000
_MAX_SEND_THRESHOLD_FIRST_TRANSACTION = 1500


_MAX_ID_POLICY_COUNTRIES = ["nigeria"]


class MaxTransactionAmountError(Exception):
    pass


class Transaction:
    send_country: str
    receive_country: str
    amount: float
    transaction_count: int


def get_id_policy(transaction_count: int, send_country: str, receive_country: str, amount: float):
    if amount > _MAX_SEND_THRESHOLD_ANY_TRANSACTION:
        raise MaxTransactionAmountError(
            f"The Amount {amount} is higher than the max limit of {_MAX_SEND_THRESHOLD_ANY_TRANSACTION}"
        )

    req_id = Required_ID.SIMPLE_VERIFICATION

    receive_country = receive_country.lower()
    if receive_country in _MAX_ID_POLICY_COUNTRIES or send_country in _MAX_ID_POLICY_COUNTRIES:
        req_id = Required_ID.SELFIE_MATCH

    elif transaction_count == 1:
        if (
            _MIN_SEND_THRESHOLD_ANY_TRANSACTION
            <= amount
            <= _MAX_SEND_THRESHOLD_FIRST_TRANSACTION / 2
        ):
            req_id = Required_ID.ID_VERIFICATION
        elif (
            _MAX_SEND_THRESHOLD_FIRST_TRANSACTION / 2
            < amount
            < _MAX_SEND_THRESHOLD_FIRST_TRANSACTION
        ):
            req_id = Required_ID.SELFIE_MATCH
        else:
            raise MaxTransactionAmountError(
                f"The Amount {amount} is higher than the first transaction max limit of {_MAX_SEND_THRESHOLD_FIRST_TRANSACTION}"
            )

    else:
        if _MAX_SEND_THRESHOLD_ANY_TRANSACTION <= amount <= _MAX_SEND_THRESHOLD_ANY_TRANSACTION / 2:
            req_id = Required_ID.ID_VERIFICATION
        elif _MAX_SEND_THRESHOLD_ANY_TRANSACTION / 2 < amount < _MAX_SEND_THRESHOLD_ANY_TRANSACTION:
            req_id = Required_ID.SELFIE_MATCH

    return req_id

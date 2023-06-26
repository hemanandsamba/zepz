from datetime import datetime
from uuid import UUID
from tkinter.filedialog import askopenfilename

from zepz.common import SimpleVerification


class IPAddress:
    ip: str  # can be ipv4 or 6
    user_id: int  # user id associated with this record
    when_created: datetime  # when this IP address was created


class Device:
    device_id: UUID  # globally unique identifier for the user
    user_id: int  # user id associated with this record
    when_created: datetime  # when this record was created


def get_latest_used_ip_address(user_id: int) -> IPAddress:
    """
    Returns the most recently used IP address associated with the user
    :param user_id: user id
    :return: IP address of the user
    """
    pass


def get_latest_device_id(user_id: int) -> Device:
    """
    Returns the most recently used device associated with the user
    :param user_id: user_id
    :return:
    """
    pass


def prompt_user_simple_verification() -> SimpleVerification:
    user_id = int(input("Enter SSN"))
    first_name = input("Enter First Name")
    middle_name = input("Enter Middle Name")
    last_name = input("Enter Last Name")
    address = input("Enter Address")
    email_id = input("Enter Email ID")
    return SimpleVerification(
        user_id, first_name, last_name, address, email_id, middle_name=middle_name
    )


def _prompt_image_file(title: str) -> str:
    file_name = askopenfilename(
        initialdir="/",
        title=title,
        filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")),
    )
    return file_name


def prompt_user_drivers_license() -> str:
    return _prompt_image_file(title="Select DL")


def prompt_user_selfie_pic() -> str:
    return _prompt_image_file(title="Select Selfie")

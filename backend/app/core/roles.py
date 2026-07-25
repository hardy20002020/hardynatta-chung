from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    PROVINCE = "PROVINCE"
    CITY = "CITY"
    MEMBER = "MEMBER"
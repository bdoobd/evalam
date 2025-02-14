from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    powered = "powered"
    user = "user"

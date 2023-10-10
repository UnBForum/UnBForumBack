import enum


class Role(str, enum.Enum):
    administrator = "administrator"
    moderator = "moderator"
    member = "member"

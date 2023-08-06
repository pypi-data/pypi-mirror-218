from enum import Enum, EnumMeta
from typing import Any


class EnumeratorMeta(EnumMeta):

    def __contains__(cls, member: Any):
        if type(member) == cls:
            return EnumMeta.__contains__(cls, member)
        else:
            try:
                cls(member)
            except ValueError:
                return False
            return True


class Enumerator(Enum, metaclass=EnumeratorMeta):
    pass

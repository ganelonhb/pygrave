from typing import Any

from .Core import Infix

from .Implements import Implement
from .CImplements import CImplement

def __implements__(cls : Any, implement : type) -> True:
    if not issubclass(implement, Implement) and not issubclass(implement, CImplement):
        raise ValueError(f"Supplied implement \'{implement.__name__}\' is not of Implement type")

    if type(cls) == type:
        return implement in cls.__mro__

    return implement in type(cls).__mro__

implements = Infix(__implements__)

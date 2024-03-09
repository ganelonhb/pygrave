"""implements are mixins that add functionality to an object"""

from typing import Any

from .infix import Infix

class Implement:
    """The implement base class does not have a Thing ID"""

    pass

def __implements__(cls : Any, implement : type) -> True:
    if not issubclass(implement, Implement):
        raise ValueError(f"Supplied implement \'{implement.__name__}\' is not of Implement type")

    if type(cls) == type:
        return implement in cls.__mro__

    return implement in type(cls).__mro__

implements = Infix(__implements__)

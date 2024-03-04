"""A function class is a class that requires the __call__ method to be defined"""

from typing import Union
from .thing import Thing

class FunctionClass(Thing):
    """The function class will require __call__ to be overridden"""
    def __call__(self, *args, **kwargs) -> Union[object, None]:
        """Crash the program when called"""
        raise NotImplementedError

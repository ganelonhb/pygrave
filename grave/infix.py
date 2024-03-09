# Adapted from https://code.activestate.com/recipes/384122/ by Ferdinand Jamitzky

"""infix operator for custom operators"""

from typing import Callable, Any

from .function_class import FunctionClass


class Infix(FunctionClass):
    """Infix class for custom operators"""

    def __init__(self, func : Callable[[Any, Any], Any]):
        self._func = func

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self._func(other, x))

    def __rshift__(self, other):
        return self._func(other)

    def __call__(self, lhs : Any, rhs: Any):
        return self._func(lhs, rhs)

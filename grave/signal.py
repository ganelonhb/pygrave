"""A signal can be used as a method by which game objects communicate with each other"""

from typing import Callable, Union, Any

from .function_class import FunctionClass


class Signal(FunctionClass):
    """Under the hood, the signal class manages slots"""

    def __init__(self, *types, before=None, after=None):
        """Initialize the signal object"""

        super().__init__()

        self._before_method = before
        self._after_method = after

        self._slots = set()

    def add_slot(self, slot : Callable[..., None]) -> None:
        """Add slots to the signal object"""
        self._slots.add(slot)

    def remove_slot(self, slot : Callable[..., None]) -> None:
        """Remove slots from the signal object"""
        self._slots.discard(slot)

    def emit(self, *args, **kwargs) -> None:
        return self.__call__(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> None:
        """Call every slot managed by the signal"""
        if self._before_method is not None:
            self._before_method(*args, **kwargs)

        for slot in self._slots:
            slot(*args, **kwargs)

        if self._after_method is not None:
            self._after_method(*args, **kwargs)



    @staticmethod
    def connect(signal : Callable[..., None], slot : Callable[..., None]):
        """Connect a slot to a signal Qt style"""

        if not callable(signal):
            raise ValueError(f"Passed object {signal} is not callable, and cannot be used as a signal.")

        if not isinstance(signal, Signal):
            raise ValueError(f"Passed method {signal} is not bound to an object, and cannot be connected to a slot.")

        signal.add_slot(slot)


    @staticmethod
    def disconnect(signal : Callable[..., None], slot : Callable[..., None]):
        """Disconnect a slot from a signal Qt style"""
        if not callable(signal):
            raise ValueError(f"Passed object {signal} is not callable, and cannot be disconnected from a slot.")

        if not isinstance(signal, Signal):
            raise ValueError(f"Passed method {signal} is not bound to an object, and cannot be disconnected from a slot.")

        signal.remove_slot(slot)



def signal(f):
    """Decorator for signals. Automatically calls the signal that shares the name as the class method"""

    return Signal(before=f)

"""A signal can be used as a method by which game objects communicate with each other"""

from typing import Callable, Union, Any

from .function_class import FunctionClass


class Signal(FunctionClass):
    """Under the hood, the signal class manages slots"""

    def __init__(self):
        """Initialize the signal object"""

        super().__init__()

        self._slots = set()

    def add_slot(self, slot : Callable[..., None]) -> None:
        """Add slots to the signal object"""
        self._slots.add(slot)

    def remove_slot(self, slot : Callable[..., None]) -> None:
        """Remove slots from the signal object"""
        self._slots.discard(slot)

    def __call__(self, *args, **kwargs) -> None:
        """Call every slot managed by the signal"""
        for slot in self._slots:
            slot(*args, **kwargs)

    @staticmethod
    def connect(obj : Any, signal : Callable[..., None], slot : Callable[..., None]):
        """Connect a slot to a signal Qt style"""
        obj.signals[signal.__name__].add_slot(slot)

    @staticmethod
    def disconnect(obj : Any, signal : Callable[..., None], slot : Callable[..., None]):
        """Disconnect a slot from a signal Qt style"""
        obj.signals[signal.__name__].remove_slot(slot)

def signal(f):
    """Decorator for signals. Automatically calls the signal that shares the name as the class method"""
    def l(cls, *args, **kwargs):
        cls.signals[f.__name__].__call__(*args, **kwargs)
        return f(cls, *args, **kwargs)

    l.__name__ = f.__name__
    l.__dict__["__PYGRAVE_SIGNAL_NAME__"] = f"__PYGRAVE_SIGNAL_{f.__name__}__"

    return l

# No need to test signals. They are tested in game_object.py

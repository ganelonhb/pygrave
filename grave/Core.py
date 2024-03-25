"""Implementations of Base classes that don't do all that much"""

from typing import Any, Callable, Union
from uuid import uuid4, UUID


class Thing:
    """Every thing has a thing_id. The thing_id identifies it in the object hierarchy."""

    def __init__(self):
        """Initialize a thing with a UUID. You can assign a custom UUID if you wish."""

        self._thing_id : UUID = uuid4()

    def thing_id(self) -> UUID:
        """Get the UUID of the thing."""

        return self._thing_id


class FunctionClass(Thing):
    """The function class will require __call__ to be overridden"""

    def __call__(self, *args, **kwargs) -> Any:
        """Crash the program when called"""
        raise NotImplementedError


# Adapted from https://code.activestate.com/recipes/384122/ by Ferdinand Jamitzky
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



class Tag(Thing):
    """A tag can assist in the creation of an ECS system."""

    def __init__(self, name: str, description: str = "", data: Any = None):
        """Initialize a tag object"""

        super().__init__()

        self._name : str = name
        self._description : str= description
        self._data : Any = data
        self._is_active : bool = True

    @property
    def name(self) -> str:
        """Getter for the tag name"""

        return self._name

    @name.setter
    def name(self, new_name : str) -> None:
        """setter for name"""
        self._name = new_name

    @property
    def description(self) -> str:
        """Getter for the tag description"""

        return self._description

    @description.setter
    def description(self, new_description : str) -> None:
        """setter for the tag description"""

        self._description = new_description

    @property
    def active(self) -> bool:
        """Getter for whether or not the tag is active"""

        return self._is_active

    @active.setter
    def active(self, is_active : bool) -> None:
        """Setter for whether or not the tag is active"""

        self._is_active = is_active

    @property
    def data(self) -> Any:
        """Getter for Tag Data"""

        return self._data

    @data.setter
    def data(self, new_data : Any) -> None:
        """Setter for tag data"""

        self._data = new_data


class GameObject(Thing):
    """Defines a kind of game object that supports a tagging system"""

    def __init__(
        self,
        name: str = None,
        active : bool = True,
        tags : dict[str, Tag] = None
        ):
        """Initialize a game object"""

        super().__init__()

        self._name : str = name if name is not None else str(uuid4())
        self._active : bool = active
        self._tags : dict[str, Tag] = dict() if tags is None else tags


    def name(self) -> str:
        """The name of the object"""

        return self._name

    def active(self) -> str:
        """Will the object be active in the scene"""

        return self._active


    def set_active(self, is_active: bool) -> None:
        """Active setter"""

        self._active = is_active

    def tags(self) -> dict[str, Tag]:
        """get the dictionary of tags"""

        return self._tags

    def tag(self, name : str) -> Tag:
        """Get the tag at the given name in the dictionary"""

        return self._tags[name]

    def add_tag(self, **kwargs) -> None:
        """Add a tag. Either use tag, or name, description, and data as args"""

        keys = kwargs.keys()

        if "tag" in keys and len(keys) == 1:
            self._tags[kwargs["tag"].name] = kwargs["tag"]
        elif "name" in keys and 1 <= len(keys) <= 3:
            name = kwargs["name"]
            desc = None if "description" not in keys else kwargs["description"]
            data = None if "data" not in keys else kwargs["data"]

            self._tags[kwargs["name"]] = Tag(name, desc, data)
        else:
            raise ValueError("Incorrect arguments passed to add_tag")


class GameObject(Thing):
    """Defines a kind of game object that supports a tagging system"""

    def __init__(
        self,
        name: str = None,
        active : bool = True,
        tags : dict[str, Tag] = None
        ):
        """Initialize a game object"""

        super().__init__()

        self._name : str = name if name is not None else str(uuid4())
        self._active : bool = active
        self._tags : dict[str, Tag] = dict() if tags is None else tags


    def name(self) -> str:
        """The name of the object"""

        return self._name

    def active(self) -> str:
        """Will the object be active in the scene"""

        return self._active


    def set_active(self, is_active: bool) -> None:
        """Active setter"""

        self._active = is_active

    def tags(self) -> dict[str, Tag]:
        """get the dictionary of tags"""

        return self._tags

    def tag(self, name : str) -> Tag:
        """Get the tag at the given name in the dictionary"""

        return self._tags[name]

    def add_tag(self, **kwargs) -> None:
        """Add a tag. Either use tag, or name, description, and data as args"""

        keys = kwargs.keys()

        if "tag" in keys and len(keys) == 1:
            self._tags[kwargs["tag"].name] = kwargs["tag"]
        elif "name" in keys and 1 <= len(keys) <= 3:
            name = kwargs["name"]
            desc = None if "description" not in keys else kwargs["description"]
            data = None if "data" not in keys else kwargs["data"]

            self._tags[kwargs["name"]] = Tag(name, desc, data)
        else:
            raise ValueError("Incorrect arguments passed to add_tag")

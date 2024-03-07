"""Every single object in a game should inherit from game_object"""

from .thing import Thing
from .tag import Tag
from .signal import Signal, signal
from .grave_tester import GraveTester

class GameObjectMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        obj._initialize_signals()
        return obj

class GameObject(Thing, metaclass=GameObjectMeta):
    """Defines a kind of game object that supports a tagging system"""

    def __init__(
        self,
        name: str,
        active : bool = True,
        tags : dict[str, Tag] = {}
        ):
        """Initialize a game object"""

        super().__init__()

        self._name : str = name
        self._active : bool = active
        self._tags : dict[str, Tag] = tags

        self.signals = {}

    def _initialize_signals(self) -> None:
        """Initialize the signals. Do not call this yourself."""

        self.signals = {
            getattr(self, func).__name__ : Signal()
            for func in dir(self)
            if (
                callable(getattr(self, func))
                and "__PYGRAVE_SIGNAL_NAME__" in dir(getattr(self, func))
                )
        }

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


class GameObjectTester(GraveTester):
    def init_game_object(self):
        a = GameObject("Test Object", tags={"Foo" : Tag("Bar")})

        tag = a.tag("Foo")

        return a.name == "Test Object" and tag.name == "Bar"

    def add_new_tags(self):
        a = GameObject("Test Object")

        a.add_tag(tag=Tag("Foo", "Bar", "FooBar"))
        a.add_tag(name="Fizz", description="Buzz", data="FizzBuzz")

        msg = None

        return (
            a.tag("Foo").description == "Bar"
            and a.tag("Foo").data == "FooBar"
            and a.tag("Fizz").description == "Buzz"
            and a.tag("Fizz").data == "FizzBuzz"
            )

    def test_signals(self):

        class SignalGameObject(GameObject):

            @signal
            def foo(self, *args, **kwargs):
                print("Hello World!")

                return True

            def bar(self, *args, **kwargs):
                if "fizz" in kwargs and kwargs["fizz"]:
                    print(f"Buzz! from {self.name}")

        a = SignalGameObject("A")
        b = SignalGameObject("B")

        Signal.connect(a, a.foo, b.bar)

        a.foo()
        a.foo(fizz=True)

        Signal.disconnect(a, a.foo, b.bar)

        return a.foo() and b.bar not in a.signals["foo"]._slots

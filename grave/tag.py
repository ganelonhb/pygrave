"""tags that can contain data of any arbitrary type"""

from .thing import Thing

from .grave_tester import GraveTester

class Tag(Thing):
    """A tag can assist in the creation of an ECS system."""

    def __init__(self, name: str, description: str = "", data: object = None):
        """Initialize a tag object"""

        super().__init__()

        self._name : str = name
        self._description : str= description
        self._data : object = data
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
    def data(self) -> object:
        """Getter for Tag Data"""

        return self._data

    @data.setter
    def data(self, new_data : object) -> None:
        """Setter for tag data"""

        self._data = new_data

class TagTester(GraveTester):
    """Test the Tag class"""
    def create_tag(self):
        """Test if initializing a tag correctly assigns data"""
        a = Tag("Test", "A test tag.", "Some arbitrary data")

        return a.name == "Test" and a.description == "A test tag." and a.data == "Some arbitrary data"

    def change_name(self):
        """Check if changing a tag name works"""
        a = Tag("Test")
        a.name = "Foo"

        return a.name == "Foo"

    def change_description(self):
        """Check if changing a tag description works"""

        a = Tag("Test", "Foo")
        a.description = "Bar"

        return a.description == "Bar"

    def change_data(self):
        """Check if changing a tag's data works"""
        a = Tag("Test", "Foo", "Bar")
        a.data = "FooBar"

        return a.data == "FooBar"

    def set_inactive(self):
        """Check if changing a tag active status works"""

        a = Tag("Test")
        a.active = False

        return not a.active

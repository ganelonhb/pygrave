"""the very basic kind of object, a thing"""

from uuid import uuid4, UUID

class Thing:
    """Every thing has a thing_id. The thing_id identifies it in the object hierarchy."""

    def __init__(self):
        """Initialize a thing with a UUID. You can assign a custom UUID if you wish."""

        self._thing_id : UUID = uuid4()

    def thing_id(self) -> UUID:
        """Get the UUID of the thing."""

        return self._thing_id

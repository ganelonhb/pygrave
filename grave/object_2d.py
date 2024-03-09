"""Object2D is a 2D object that can be drawn to the screen"""

from .game_object import GameObject


class Object2D(GameObject):
    """Object2D is a 2D object that can be drawn to the screen"""

    def draw(self) -> None:
        """Implementation of Draw is required."""

        raise NotImplementedError

    def update(self) -> None:
        """Update the Object2D in the scene"""

        raise NotImplementedError

    def collide(self):
        """return the list of collision rectangles"""

        raise NotImplementedError

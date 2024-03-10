"""Object2D is a 2D object that can be drawn to the screen"""

from .implement import Implement


class ImplementsSprite(Implement):
    """Object2D is a 2D object that can be drawn to the screen"""

    _surface = None

    def draw(self) -> None:
        """Implementation of Draw is required."""

        raise NotImplementedError

    def update(self) -> None:
        """Update the Object2D in the scene"""

        raise NotImplementedError

    def collide(self):
        """return a list of rects that determine collisions"""

        raise NotImplementedError

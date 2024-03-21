"""Object2D is a 2D object that can be drawn to the screen"""

from pygame import Rect

from .implement import Implement

class ImplementsSprite(Implement):
    """Object2D is a 2D object that can be drawn to the screen"""

    _surface = None
    _image = None

    @property
    def rect(self) -> Rect:
        return None if self._image is None else Rect(self.x, self.y, self._image.get_width(), self._image.get_height())

    def draw(self) -> None:
        """Implementation of Draw is required."""

        raise NotImplementedError

    def update(self) -> None:
        """Update the Object2D in the scene"""

        raise NotImplementedError

    def collide(self) -> list[Rect]:
        """return a list of rects that determine collisions"""

        raise NotImplementedError

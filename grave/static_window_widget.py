"""A static window widget appears on the screen and does not move"""

from .widget import Widget
from .implements_position import ImplementsPosition

class StaticWindowWidget(Widget, ImplementsPosition):
    def __init__(
        self,
        parent = None,
        surface = None,
        image = None,
        position : tuple[int, int] = (0, 0),
        name : str = None,
        active : bool = True,
        tags = dict(),
        ):
        super().__init__(name, surface, active, tags)

        self._x = position[0] + (0 if parent is None else parent.x)
        self._y = position[1] + (0 if parent is None else parent.y)

        self._image = image

    def draw(self) -> None:
        if self.active:
            self._surface.blit(self._image, self.position)
            super().draw()


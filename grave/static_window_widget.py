"""A static window widget appears on the screen and does not move"""

from .widget import Widget
from .implements_position import ImplementsPosition

class StaticWindowWidget(Widget, ImplementsPosition):
    def __init__(
        self,
        parent = None,
        image = None,
        position : tuple[int, int] = (0, 0),
        name : str = None,
        active : bool = True,
        tags = dict(),
        ):
        super().__init__(name, active, tags)

        self._x = position[0] + (0 if parent is None else parent.x)
        self._y = position[1] + (0 if parent is None else parent.y)

        self._image = image
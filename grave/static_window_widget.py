"""A static window widget appears on the screen and does not move"""

from pygame import BLEND_RGBA_MULT
from pygame.mask import from_surface

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
        tags = None,
        ):

        super().__init__(parent, surface, name, active, tags)

        self._x = position[0] + (0 if parent is None else parent.x)
        self._y = position[1] + (0 if parent is None else parent.y)

        self._image = image

        self._mask = from_surface(self._image)

        o_x = None if parent is None else parent.x - self.x
        o_y = None if parent is None else parent.y - self.y
        self._overlap_mask = None if parent is None else self.mask.overlap_mask(parent.mask, (o_x, o_y))

    def draw(self) -> None:
        if self.active:
            if self._overlap_mask is None:
                image = self._image
            else:
                image = self._overlap_mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255))
                image.blit(self._image, (0,0), special_flags=BLEND_RGBA_MULT)

            self._surface.blit(image, self.position)
        super().draw()

    def update(self) -> None:
        o_x = None if self._parent is None else self._parent.x - self.x
        o_y = None if self._parent is None else self._parent.y - self.y

        self._overlap_mask = None if self._parent is None else self.mask.overlap_mask(self._parent.mask, (o_x, o_y))

        super().update()

    @property
    def image(self):
        return self._image

    @property
    def mask(self):
        return self._mask

    def set_overlap_mask(self, mask):
        self._overlap_mask = mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255))

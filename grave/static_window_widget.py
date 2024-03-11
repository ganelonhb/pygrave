"""A static window widget appears on the screen and does not move"""

from pygame import BLEND_RGBA_MULT

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

        self._mask = pygame.mask.from_surface(self._image)

        self._overlap_mask = None if parent is None else None

    def draw(self) -> None:
        if self.active:
            if self._overlap_mask is None:
                image = self._image
            else:
                image = self._overlap_mask.copy()
                image.blit(self._image, (0,0), special_flags=BLEND_RGBA_MULT)

            self._surface.blit(image, self.position)
            super().draw()

    def set_overlap_mask(self, mask):
        self._overlap_mask = mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255))

    @property
    def image(self):
        return self._image

    @property
    def mask(self):
        return self._mask

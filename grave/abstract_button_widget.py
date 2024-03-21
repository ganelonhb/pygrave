"""serve as the base class for all buttons"""

from pygame import BLEND_RGBA_MULT
from pygame.mask import from_surface
from pygame import MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, mouse

from .widget import Widget
from .implements_position import ImplementsPosition
from .signal import Signal



class AbstractButtonWidget(Widget, ImplementsPosition):
    """the abstract button widget will serve as a base class for any button"""

    def __init__(
        self,
        text : str = "",
        parent = None,
        name : str = "Button",
        surface = None,
        image = None,
        position : tuple[int, int] = (0, 0),
        active : bool = True,
        tags = None
        ):

        super().__init__(parent, surface, name, active, tags)

        self._x = position[0] + (0 if parent is None else parent.x)
        self._y = position[1] + (0 if parent is None else parent.y)

        self._image = image

        self._mask = from_surface(self._image)

        o_x = None if parent is None else parent.x - self.x
        o_y = None if parent is None else parent.y - self.y
        self._overlap_mask = None if parent is None else self._mask.overlap_mask(parent._mask, (o_x, o_y))
        self._hovering = False
        self._pressed = False

    on_pressed = Signal(None)
    on_released = Signal(None)
    on_clicked = Signal(None)
    on_hover = Signal(None)
    on_hover_exit = Signal(None)

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

        self._overlap_mask = None if self._parent is None else self._mask.overlap_mask(self._parent.mask, (o_x, o_y))

        super().update()

    def process_events(self, event):

        super().process_events(event)

        m_x, m_y = mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN and (
            self.rect is not None
            and self.rect.collidepoint(m_x, m_y)
            ):
            if not self._pressed:
                self._pressed = True

            self.on_pressed.emit()
        elif event.type == MOUSEBUTTONUP and self.rect is not None:
            if self.rect.collidepoint(m_x, m_y):
                if self._pressed:
                    self._pressed = False
                    self.on_clicked.emit()

                self.on_released.emit()
            else:
                if self._pressed:
                    self._pressed = False

            self.on_released.emit()
        elif event.type == MOUSEMOTION and self.rect is not None:
            e_x, e_y = event.pos
            if not self._hovering and self.rect.collidepoint(e_x, e_y):
                self._hovering = True
                self.on_hover.emit()
            elif self._hovering and not self.rect.collidepoint(e_x, e_y):
                self._hovering = False
                self.on_hover_exit.emit()





# Signal Ideas:
# on_pressed
# on_released
# on_hover

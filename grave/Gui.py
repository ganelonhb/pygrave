from pygame import Rect, BLEND_RGBA_MULT, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, mouse
from pygame.mask import from_surface

from .Core import GameObject, Signal
from .Implements import ImplementsSprite, ImplementsPosition


class Widget(GameObject, ImplementsPosition, ImplementsSprite):
    """A drawable that has subwidgets"""

    def __init__(
        self,
        parent = None,
        surface = None,
        name : str = None,
        active : bool = True,
        tags = None
        ):
        super().__init__(name, active, tags)

        self._parent = parent
        self._widgets = set()
        self._surface = surface

    def _set_parent(self, parent):
        self._parent = parent

    def draw(self) -> None:
        """draw all subwidgets of this widget."""

        for widget in self._widgets:
            widget.draw()

    def update(self) -> None:
        """update all subwidgets of this widget."""

        for widget in self._widgets:
            widget.update()

    def add_widget(self, widget) -> None:
        """add a widget to the list of widgets"""

        self._widgets.add(widget)
        widget._set_parent(self)
        widget.set_position(widget.x + self.x, widget.y + self.y)

    def process_events(self, event) -> None:
        for widget in self._widgets:
            widget.process_events(event)


    def remove_widget(self, widget) -> bool:
        """remove a widget from the list of widgets"""

        if widget not in self._widgets:
            return False

        self._widgets.remove(widget)

        return True


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

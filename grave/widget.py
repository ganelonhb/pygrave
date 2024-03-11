"""A widget is a drawable that has subwidgets"""

from .game_object import GameObject
from .implements_sprite import ImplementsSprite
from .implements_position import ImplementsPosition


class Widget(GameObject, ImplementsPosition, ImplementsSprite):
    """A drawable that has subwidgets"""

    def __init__(
        self,
        parent = None,
        surface = None,
        name : str = None,
        active : bool = True,
        tags = dict()
        ):
        super().__init__(name, active, tags)

        self._parent = parent
        self._widgets = set()
        self._surface = surface

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

    def remove_widget(self, widget) -> bool:
        """remove a widget from the list of widgets"""

        if widget not in self._widgets:
            return False

        self._widgets.remove(widget)

        return True

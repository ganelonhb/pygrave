"""A widget is a drawable that has subwidgets"""

from .object_2d import Object2D


class Widget(Object2D):
    """A drawable that has subwidgets"""

    def __init__(
        self,
        parent = None,
        name : str = None,
        active : bool = True,
        tags = dict()
        ):
        super().__init__(name, active, tags)

        self._parent = parent
        self._widgets = set()

    def draw(self) -> None:
        """draw all subwidgets of this widget."""

        for widget in self._widgets:
            widget.draw()

    def add_widget(self, widget) -> None:
        """add a widget to the list of widgets"""

        self._widgets.add(widget)

    def remove_widget(self, widget) -> bool:
        """remove a widget from the list of widgets"""

        if widget not in self._widgets:
            return False

        self._widgets.remove(widget)

        return True
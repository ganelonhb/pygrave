"""Implement that ensures a position vector exists"""

from .implement import Implement


class ImplementsPosition(Implement):
    """Implment a 2D position vector"""

    _x : int = 0
    _y : int = 0

    @property
    def position(self) -> tuple[int, int]:
        """Get X and Y as a tuple"""

        return (self._x, self._y)

    @position.setter
    def position(self, xy : tuple[int, int]) -> None:
        """set X and Y"""

        self._x, self._y = xy[0], xy[1]

    def set_position(self, x : int, y : int) -> None:
        """set X and Y"""

        self._x, self._y = x, y
    
    @property
    def x(self) -> int:
        """get the x position"""

        return self._x

    @x.setter
    def x(self, X : int) -> None:
        """set the x position"""

        self._x = X

    @property
    def y(self) -> int:
        """get the y position"""

        return self._y

    @y.setter
    def y(self, Y : int) -> None:
        """set the y position"""

        self._y = Y
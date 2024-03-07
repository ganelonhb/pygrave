"""Implement that ensures a position vector exists"""

from .implement import Implement


class ImplementsPosition(Implement):
    """Implment a 2D position vector"""

    self._x : float = 0.0
    self._y : float = 0.0

    @property
    def position(self) -> tuple[float, float]:
        """Get X and Y as a tuple"""

        return (self._x, self._y)

    @position.setter
    def position(self, xy : tuple[float, float]) -> None:
        """set X and Y"""

        self._x, self._y = xy[0], xy[1]

    def set_position(self, x : float, y : float) -> None:
        """set X and Y"""

        self._x, self._y = x, y
    
    @property
    def x(self) -> float:
        """get the x position"""

        return self._x

    @x.setter
    def x(self, X : float) -> None:
        """set the x position"""

        self._x = X

    @property
    def y(self) -> float:
        """get the y position"""

        return self._y

    @y.setter
    def y(self, Y : float) -> None:
        """set the y position"""

        self._y = Y
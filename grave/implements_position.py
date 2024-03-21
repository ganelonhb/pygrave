"""Implement that ensures a position vector exists"""

from .implement import Implement

class ImplementsPosition(Implement):
    """Implment a 2D position vector"""

    _x : int = 0
    _y : int = 0

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def set_x(self, x : int) -> None:
        self._x = x

    def set_y(self, y : int) -> None:
        self._y = y

    def set_position(self, x : int, y : int) -> None:
        """set X and Y"""

        self._x, self._y = x, y


    @property
    def position(self) -> tuple[int, int]:
        """Get X and Y as a tuple"""

        return (int(self._x), int(self._y))

    @position.setter
    def position(self, xy : tuple[int, int]) -> None:
        """set X and Y"""

        self._x, self._y = xy
    
    @property
    def x(self) -> int:
        """get the x position"""

        return self._x

    @x.setter
    def x(self, X : int) -> None:
        """set the x position"""

        self.set_x(X)

    @property
    def y(self) -> int:
        """get the y position"""

        return self._y

    @y.setter
    def y(self, Y : int) -> None:
        """set the y position"""

        self.set_y(Y)

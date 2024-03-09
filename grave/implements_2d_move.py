"""Implement that ensures movement and roation in 2d can occur"""

from .implements_position import ImplementsPosition


class Implements2DMove(ImplementsPosition):
    """implements methods to manipulate position"""

    _angle : float = 0

    def move(self, x : float, y : float) -> None:
        """move in x and y direction"""

        self._x = int(self._x + x)
        self._y = int(self._y + y)

    def move_and_roate(self, x : float, y : float, theta_rads : float) -> None:
        """move and rotate at the same time"""

        self._x = int(self._x + x)
        self._y = int(self._y + y)
        self._angle += theta_rads


    def move_x(self, x : float) -> None:
        """move in the x direction"""

        self._x = int(self._x + x)

    def move_y(self, y : float) -> None:
        """move in the y direction"""

        self._y = int(self._y + y)

    def rotate(self, theta_rads : float) -> None:
        """rotate in the direction"""

        self._angle += theta_rads

    @property
    def angle(self) -> float:
        """get the angle of rotation"""

        return self._angle

    @angle.setter
    def angle(self, theta_rads : float) -> None:
        """set the angle of rotation"""

        return self._angle

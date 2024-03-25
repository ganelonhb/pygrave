"""implements are mixins that add functionality to an object"""

from pygame import Rect

class Implement:
    """The implement base class does not have a Thing ID"""

    def __init__(self, *args, **kwargs):
        self.validate()

    def validate(self):
        pass


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


class ImplementsSprite(Implement):
    """Object2D is a 2D object that can be drawn to the screen"""

    _surface = None
    _image = None

    @property
    def rect(self) -> Rect:
        return None if self._image is None else Rect(self.x, self.y, self._image.get_width(), self._image.get_height())

    def draw(self) -> None:
        """Implementation of Draw is required."""

        raise NotImplementedError

    def update(self) -> None:
        """Update the Object2D in the scene"""

        raise NotImplementedError

    def collide(self) -> list[Rect]:
        """return a list of rects that determine collisions"""

        raise NotImplementedError

"""An animation has the play method"""

from .game_object import GameObject


class Animation(GameObject):
    """An animation requires implementation of the play method"""

    def __init__(self, clock, frame_rate):
        self._clock = clock
        self._frame_rate = frame_rate

    def play(self, obj : GameObject, *args, **kwargs) -> None:
        """play this animation"""

        raise NotImplementedError

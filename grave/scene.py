"""Scene Objects for making games with PyGrave"""

import pygame

from time import time
from typing import Any
from uuid import uuid4

from .game_object import GameObject
from .signal import signal

class Scene(GameObject):
    """Base class for making PyGrave Scenes"""

    def __init__(
        self,
        screen,
        global_things,
        name="Scene"
    ):
        """scene initializer"""
        super().__init__(f"{name}_{uuid4()}")

        self._screen = screen
        self._global_things = global_things
        self._frame_rate = 60 if "frame_rate" not in global_things else global_things["frame_rate"]
        self._is_valid = True
        self._quit = False
        self._timestart = time()

    @signal
    def quit_game(self):
        pass

    def clock(self) -> None:
        """Reset the scene clock."""

        self._timestart = time()

    def draw(self) -> None:
        """draw the scene."""

        pass

    def process_event(self, event) -> None:
        """Process PyGame events in the scene."""

        if event.type == pygame.QUIT:
            self._quit = True
            self._is_valid = False

    @property
    def is_valid(self) -> bool:
        """Is the scene valid?"""

        return self._is_valid

    @is_valid.setter
    def is_valid(self, valid : bool) -> None:
        """setter for is_valid"""

        self._is_valid = valid

    @property
    def frame_rate(self) -> int:
        """return the frame rate of the scene"""

        return self._frame_rate

    def update_scene(self) -> None:
        """update the scene"""

        pass

    def start_scene(self) -> None:
        """Start the scene"""

        pass

    def end_scene(self):
        """end the scene"""

        if self._quit:
            self.quit_game()
            return ["QUIT_GAME"]

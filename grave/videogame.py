"""A game object to base your videogame off of"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import warnings

from .pygrave_constants import GRAVE_DIR
from .game_object import GameObject
from .scene import Scene

class VideoGame(GameObject):
    """Base class for creating PyGrave games"""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        surface_flags: int = pygame.HWSURFACE | pygame.DOUBLEBUF,
        window_title: str = "PyGrave Game",
        icon_path: str = os.path.join(GRAVE_DIR, "res", "icon.png"),
        global_things : dict[str, object]= None,
        ):
        """Initialize a new game"""

        pygame.init()
        pygame.joystick.init()

        self._window_size: tuple[int, int] = (width, height)
        self._clock: pygame.time.Clock = pygame.time.Clock()

        self._screen: pygame.surface.Surface = pygame.display.set_mode((width, height), surface_flags)

        self._title: str = window_title
        pygame.display.set_caption(window_title)

        self._game_over: bool = False

        if not pygame.font:
            warnings.warn("Fonts is disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound is disabled.", RuntimeWarning)

        self._global_things : dict[str, Thing] = {f"{window_title}": self}

        if global_things is not None:
            for k, v in global_things.items():
                self._global_things[k] = v

        pygame.display.set_icon(
            pygame.transform.scale(
                pygame.image.load(icon_path),
                (128, 128)
                )
            )


    def __call__(self) -> int:
        """alias of run() to allow calling of videogames"""
        return self.run()

    def run(self) -> int:
        """run the main game loop"""

        raise NotImplementedError

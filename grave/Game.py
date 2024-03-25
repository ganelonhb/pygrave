import sys
import os
import importlib

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import re
import warnings

from time import time
from typing import Callable, Any, Union
from uuid import uuid4

from .Constants import GRAVE_DIR
from .Core import GameObject, Signal


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


    quit_game = Signal(None)

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


class VideoGame(GameObject):
    """Base class for creating PyGrave games"""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        surface_flags: int = pygame.HWSURFACE | pygame.DOUBLEBUF,
        window_title: str = "PyGrave Game",
        icon_path: str = os.path.join(GRAVE_DIR, "res", "icon.png"),
        global_things : dict[str, Any]= None,
        ):
        """Initialize a new game"""

        pygame.init()
        pygame.joystick.init()

        self._window_size: tuple[int, int] = (width, height)
        self._clock: pygame.time.Clock = pygame.time.Clock()

        self._screen = pygame.display.set_mode((width, height), surface_flags)

        self._title: str = window_title
        pygame.display.set_caption(window_title)

        self._game_over: bool = False

        if not pygame.font:
            warnings.warn("Fonts is disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound is disabled.", RuntimeWarning)

        self._global_things : dict[str, Thing] = {"root": self, "clock": self._clock}

        if global_things is not None:
            for k, v in global_things.items():
                self._global_things[k] = v

        pygame.display.set_icon(
            pygame.transform.scale(
                pygame.image.load(icon_path),
                (128, 128)
                )
            )

    def window_title(self):
        return self._title

    def window_size(self):
        return self._window_size

    def screen(self):
        return self._screen

    def __call__(self) -> int:
        """alias of run() to allow calling of videogames"""
        return self.run()

    def run(self) -> int:
        """run the main game loop"""

        raise NotImplementedError


class SceneDictVideogame(VideoGame):
    """a videogame powered by a scene dict"""

    def __init__(
        self,
        width : int = 800,
        height : int = 600,
        surface_flags : int = pygame.HWSURFACE | pygame.DOUBLEBUF,
        window_title : str = "PyGrave Game",
        icon_path : str = os.path.join(GRAVE_DIR, "res", "icon.png"),
        global_things : Union[dict[str, Any], None] = None,
        scene_dir_list : list[str] = [],
        game_module_override : str = "grave",
        first_level_override : Union[str, None] = None,
        custom_level_sorting_key : str = str.casefold
        ):
        """initialize a SceneDictVideogame"""

        super().__init__(width, height, surface_flags, window_title, icon_path, global_things)

        levels : list[str] = []

        for level_dir in scene_dir_list:
            levels += [os.path.join(level_dir, level) for level in os.listdir(level_dir) if re.match(r'.+_scene\.py', level, flags=re.UNICODE)]

        levels = sorted(levels, key=custom_level_sorting_key)

        level_modules = dict()
        self._level_classes : dict[str, Scene] = dict()

        to_classname : Callable[str, str] = lambda s : f"{s[0].upper()}{s[1:]}"

        for level in levels:
            module_name, _ = os.path.splitext(os.path.basename(level))

            module_loc : str = f"{game_module_override}.{module_name}"

            spec = importlib.util.spec_from_file_location(module_loc, level)

            level_modules[module_loc] = importlib.util.module_from_spec(spec)


            sys.modules[module_loc] = level_modules[module_loc]

            spec.loader.exec_module(level_modules[module_loc])

            class_name : str = ''.join([to_classname(fname) for fname in module_name.split('_')])

            self._level_classes[class_name] = getattr(sys.modules[module_loc], class_name)
            if not issubclass(self._level_classes[class_name], Scene):
                raise ValueError(f"{class_name} is not a Pygrave Scene")

        if first_level_override is not None and first_level_override in self._level_classes:
            self._first_level = first_level_override
        else:
            self._first_level = None if len(self._level_classes.keys()) == 0 else sorted(self._level_classes.keys(), key=custom_level_sorting_key)[0]


        self._scene_dict = dict()
        self.build_scene_dict()

    def quit_game(self) -> None:
        self._game_over = True

    def reinitialize_level(self, level_name : str) -> None:
        """reinitialize the level with the given name"""

        LevelClass = self._level_classes[level_name]
        del self._scene_dict[level_name]
        self._scene_dict[level_name] = LevelClass(self._screen, self._global_things)

    def build_scene_dict(self) -> None:
        """build the game's scene dict"""

        for level_name, LevelClass in self._level_classes.items():
            self._scene_dict[level_name] = LevelClass(self._screen, self._global_things)
            Signal.connect(self._scene_dict[level_name].quit_game, self.quit_game)

    def run(self) -> int:
        """run the game loop"""

        scene_dict = self._scene_dict
        current_scene_string = self._first_level

        while not self._game_over:
            current_scene = scene_dict[current_scene_string]
            current_scene.clock()
            current_scene.start_scene()

            while current_scene.is_valid:
                self._clock.tick(current_scene.frame_rate)
                for event in pygame.event.get():
                    current_scene.process_event(event)
                current_scene.update_scene()
                current_scene.draw()
                pygame.display.flip()
            command = current_scene.end_scene()

            match command:
                case ['QUIT_GAME']:
                    self._game_is_over = True
                case ['CHANGE_SCENE', scene_name]:
                    self.reinitialize_level(current_scene_string)
                    current_scene_string = scene_name

        pygame.quit()
        return 0

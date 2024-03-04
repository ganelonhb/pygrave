"""module implements a videogame with a game loop that is managed by a dictionary of scenes"""

import sys
import os
import importlib

import pygame

import re

from typing import Callable, Union

from .pygrave_constants import GRAVE_DIR
from .videogame import VideoGame
from .scene import Scene

class SceneDictVideogame(VideoGame):
    def __init__(
        self,
        width : int = 800,
        height : int = 600,
        surface_flags : int = pygame.HWSURFACE | pygame.DOUBLEBUF,
        window_title : str = "PyGrave Game",
        icon_path : str = os.path.join(GRAVE_DIR, "res", "icon.png"),
        global_things : dict[str, object] = None,
        level_dir_list : list[str] = [],
        game_module_override : str = "grave",
        first_level_override : Union[str, None] = None,
        custom_level_sorting_key : str = str.casefold
        ):
        super().__init__(width, height, surface_flags, window_title, icon_path, global_things)

        levels : list[str]= []

        for level_dir in level_dir_list:
            levels += [os.path.join(level_dir, level) for level in os.listdir(level_dir) if re.match(r'.+_scene\.py', level, flags=re.UNICODE)]

        levels = sorted(levels, key=custom_level_sorting_key)

        level_modules = dict()
        self._level_classes : dict[str, Scene] = dict()

        to_classname : Callable[str, str] = lambda s : f"{s[0].upper()}{s[1:]}"

        for level in levels:
            module_name, _ = os.path.splitext(os.path.basename(level))

            module_loc = f"{game_module_override}.{module_name}"

            spec = importlib.util.spec_from_file_location(module_loc, level)

            level_modules[module_loc] = importlib.util.module_from_spec(spec)


            sys.modules[module_loc] = level_modules[module_loc]

            spec.loader.exec_module(level_modules[module_loc])

            class_name = ''.join([to_classname(fname) for fname in module_name.split('_')])
            print(class_name)

            self._level_classes[class_name] = getattr(sys.modules[module_loc], class_name)
            if not issubclass(self._level_classes[class_name], Scene):
                raise ValueError(f"{class_name} is not a Pygrave Scene")

        if first_level_override is not None and first_level_override in self._level_classes.keys():
            self._first_level = first_level_override
        else:
            self._first_level = None if len(self._level_classes.keys()) == 0 else sorted(self._level_classes.keys(), key=custom_level_sorting_key)[0]


        self._scene_dict = dict()
        self.build_scene_dict()

    def reinitialize_level(self, level_name : str) -> None:
        LevelClass = self._level_classes[level_name]
        del self._scene_dict[level_name]
        self._scene_dict[level_name] = LevelClass(self._screen, self._global_things)

    def build_scene_dict(self) -> None:
        for level_name, LevelClass in self._level_classes.items():
            self._scene_dict[level_name] = LevelClass(self._screen, self._global_things)

    def run(self) -> int:
        scene_dict = self._scene_dict
        current_scene_string = self._first_level

        return 0





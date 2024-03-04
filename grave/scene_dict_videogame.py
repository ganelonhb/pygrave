"""module implements a videogame with a game loop that is managed by a dictionary of scenes"""

import sys
import os
import importlib

import pygame

import re

from typing import Callable

from .pygrave_constants import GRAVE_DIR
from .videogame import VideoGame

class SceneDictVideogame(VideoGame):
    def __init__(
        self,
        width : int = 800,
        height : int = 600,
        surface_flags : int = pygame.HWSURFACE | pygame.DOUBLEBUF,
        window_title : str = "PyGrave Game",
        icon_path : str = os.path.join(GRAVE_DIR, "res", "icon.png"),
        global_things : dict[str, object] = None
        level_dir_list : list[str] = [],
        game_module_override : str = "pygrave",
        custom_level_sorting_key : str = str.casefold
        ):
        super().__init__(width, height, surface_flags, window_title, icon_path, global_things)

        levels = []

        for level_dir in level_dir_list:
            levels += [os.path.join(level_dir, level) for level in os.listdir(level_dir) if re.match(r'level_[\X{}]+.py', level)]

        levels = sorted(levels, key=custom_level_sorting_key)

        level_modules = dict()
        self._level_classes = dict()

        to_classname = lambda s : return f"{s[0].upper()}{s[1:]}"

        for level in levels:
            module_name, _ = os.path.splitext(os.path.basename(level)[6:])

            module_loc = f"{game_module_override}.{module_name}"

            spec = importlib.util.spec_from_file_location(module_loc, level)

            level_modules[module_loc] = importlib.util.module_from_spec(spec)

            sys.modules[module_loc] = level_modules[module_loc]

            spec.loader.exec_module(level_modules[module_loc])

            class_name = ''.join([to_classname(fname) for fname in module_name.split('_')])

            self._level_classes[class_name] = getattr(sys.modules[module_loc], class_name)

        self._first_level = sorted(self._level_classes.keys(), key=custom_level_sorting_key)[0]

        self.build_scene_dict()

    def reinitialize_level(self, level_name):
        LevelClass = self._level_classes[level_name]
        del self._scene_dict[level_name]
        self._scene_dict[level_name] = LevelClass(self._screen, self._global_things)

    def build_scene_dict(self):
        for level_name, LevelClass in self._level_classes.items():
            self._scene_dict[level_name] = LevelClass(self._screen, self._global_things)

    def run(self):
        scene_dict = self._scene_dict
        current_scene_string = self._first_level





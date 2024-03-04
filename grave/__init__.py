"""Init file for the grave package."""

# Any module file in the current directory of this file will
# be added to a list if it does not begin with an underscore.

from os import listdir, path

_GRAVE_this = path.split(path.abspath(__file__))[0]
_GRAVE_file_list = listdir(_GRAVE_this)
_GRAVE_exclude = [
    f
    for f in _GRAVE_file_list
    if f.startswith("_")
    ]

_GRAVE_modules = [
            path.splitext(f)[0]
            for f in _GRAVE_file_list
            if (f not in _GRAVE_exclude and path.splitext(f)[1] == ".py")
            ]

__all__ = sorted(_GRAVE_modules)

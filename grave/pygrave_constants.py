"""Constants used in PyGrave"""

from os import path
from sys import platform

# PyGrave info

GRAVE_VERSION_NAME  = "ALEPH"
GRAVE_VERSION_NUM   = "0.0.0"
GRAVE_SUBVERSION    = "α"


# Paths

UNIX_SYSTEMS = ["aix", "darwin", "freebsd", "linux", "openbsd"]
WINDOWS_SYSTEMS = ["win32", "win64", "cygwin", "msys", "nt"]

GRAVE_DIR, _        = path.split(path.abspath(__file__))

GRAVE_HOME          = path.abspath(path.expanduser('~'))
GRAVE_PROGRAMDATA   = path.abspath(
    path.join(GRAVE_HOME, '.config')
    if platform in UNIX_SYSTEMS else
    path.join(GRAVE_HOME, 'AppData', 'Local')
    )

# Numbers

GRAVE_MAGIC_NUMBER  = int(0x045C_045C)    # Use me for magic stuff.

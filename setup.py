import sys
from cx_Freeze import setup, Executable

import __version__

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "platform", "win32api"], 
    "excludes": ["tkinter"],
    "include_msvcr": True
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = __version__.ProgramName,
        version = __version__.Version,
        description = __version__.Description,
        options = {"build_exe": build_exe_options},
        executables = [Executable("trl_scu_main.py", base=base)])
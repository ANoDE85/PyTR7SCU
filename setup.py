import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "platform", "win32api"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "trl_scu",
        version = "0.1",
        description = "TR Legend SCU",
        options = {"build_exe": build_exe_options},
        executables = [Executable("trl_scu_main.py", base=base)])
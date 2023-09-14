import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["tkinter"], "excludes": []}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" for GUI applications on Windows

executables = [Executable("view_image_processor.py", base=base)]

setup(
    name="Image Processor",
    version="1.0.0",
    description="Your application description",
    options={"build_exe": build_exe_options},
    executables=executables
)

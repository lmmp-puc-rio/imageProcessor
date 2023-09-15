import sys
from cx_Freeze import setup, Executable

# Specify the icon file path
icon_file = "/home/renan/Repositorio/imageProcessor/src/images/lmmp_200x65.ico"  # Replace with the path to your icon file


# Define build_exe_options with packages and the include_files list
build_exe_options = {
    "packages": ["tkinter", "matplotlib", "numpy", "PIL", "skimage", "utils", "os", "cv2"],
    "excludes": ["" ],
    "include_files": ("/home/renan/Repositorio/imageProcessor/src", "src"),
}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [Executable(
    "/home/renan/Repositorio/imageProcessor/view_image_processor.py",
    base = base,
    icon=icon_file,
    shortcut_name="Image Processor",
    shortcut_dir= "image_processor",
    target_name = "Image Processor",
    ),
    ]

setup(
    name="Image Processor",
    version="1.0.0",
    description="",
    executables=executables,
    options={
        "build_exe": build_exe_options, 
        },    
    )     

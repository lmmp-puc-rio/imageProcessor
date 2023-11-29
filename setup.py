import sys
from cx_Freeze import setup, Executable

# Specify the icon file path
icon_file = "src/images/logo_icon.ico"  # Replace with the path to your icon file


# Define build_exe_options with packages and the include_files list
build_exe_options = {
    "packages": ["tkinter", "matplotlib", "numpy", "PIL", "skimage", "utils", "os", "cv2", "tkinter.font"],
    "excludes": [""],
    "include_files": ("src", "src"),
}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [Executable(
    "view_image_processor.py",
    base = base,
    icon=icon_file,
    shortcut_name="Image Processor",
    shortcut_dir= "image_processor",
    ),
    ]

setup(
    name="Image Processor",
    version="1.1.0",
    description="The application is used to process images, binarize them, and create histograms of the images.",
    executables=executables,
    options={
        "build_exe": build_exe_options, 
        },    
    )     

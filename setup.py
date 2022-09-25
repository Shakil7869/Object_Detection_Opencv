
from cx_Freeze import setup, Executable

setup(name = "Simple Object Detection Software",
      version = "1.0",
        description = "Simple Object Detection Software",
        executables = [Executable("main.py")])


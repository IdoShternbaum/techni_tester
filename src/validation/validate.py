from pathlib import Path

CMAKE_TXT = "CMakeLists.txt"
CMAKE_DEBUG = "cmake-build-debug"
COMPILE_CMD = "compile_commands.json"


class Validate:
    def __init__(self):
        self.proj_path = Path.cwd()
        self.cmake_txt = self.proj_path / CMAKE_TXT
        self.cmake_debug = self.proj_path / CMAKE_DEBUG
        self.cmpl_cmd_path = self.cmake_debug / COMPILE_CMD

    def check(self) -> bool:
        if not self.cmake_txt.is_file():
            raise FileNotFoundError(
                f"CMakeLists.txt not found: {self.cmake_txt}"
            )

        if not self.cmake_debug.is_dir():
            raise NotADirectoryError(
                f"CMake build directory not found: {self.cmake_debug}"
            )

        if not self.cmpl_cmd_path.is_file():
            raise FileNotFoundError(
                f"Compilation database not found: {self.cmpl_cmd_path}"
            )

        return True
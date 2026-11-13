from pathlib import Path

from test_validation import TestValidator

CMAKE_TXT = "CMakeLists.txt"
CMAKE_DEBUG = "cmake-build-debug"
CMAKE_CACHE = "CMakeCache.txt"


class Validate:
    def __init__(self, project_path=None):
        self.proj_path = Path(project_path).resolve() if project_path else Path.cwd()
        self.cmake_txt = self.proj_path / CMAKE_TXT
        self.cmake_debug = self.proj_path / CMAKE_DEBUG
        self.cache_path = self.cmake_debug / CMAKE_CACHE

    def check(self) -> bool:
        if not self.cmake_txt.is_file():
            raise FileNotFoundError(
                f"CMakeLists.txt not found: {self.cmake_txt}"
            )

        if not self.cmake_debug.is_dir():
            raise NotADirectoryError(
                f"CMake build directory not found: {self.cmake_debug}"
            )

        if not self.cache_path.is_file():
            raise FileNotFoundError(
                f"CMake cache not found: {self.cache_path}"
            )

        TestValidator(self.proj_path).check()
        return True

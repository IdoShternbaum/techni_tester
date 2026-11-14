from pathlib import Path

from validation import Validate


class Configure(Validate):
    def __init__(self, project_path=None):
        super().__init__(project_path)
        self.check()
        self.cmake_command = self.find_cmake()
        self.compiler = self.find_compiler()

    def find_compiler(self):
        with self.cache_path.open("r", encoding="utf-8-sig") as cache:
            for line in cache:
                if line.startswith("CMAKE_C_COMPILER:FILEPATH="):
                    value = line.rstrip("\r\n").partition("=")[2]
                    return Path(value) if value else None
        return None

    def find_cmake(self) -> Path:
        with self.cache_path.open("r", encoding="utf-8-sig") as cache:
            for line in cache:
                if line.startswith("CMAKE_COMMAND:INTERNAL="):
                    value = line.rstrip("\r\n").partition("=")[2]
                    if not value:
                        break
                    cmake = Path(value)
                    if not cmake.is_file():
                        raise FileNotFoundError(
                            f"CMake executable recorded in {self.cache_path} "
                            f"does not exist: {cmake}"
                        )
                    return cmake
        raise ValueError(f"CMAKE_COMMAND not found in CMake cache: {self.cache_path}")

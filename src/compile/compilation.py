import json
import subprocess
from pathlib import Path
from configuration import Configure


class Compile(Configure):
    def __init__(self):
        super().__init__()
        self.result = self.compile()

    def compile(self):
        return subprocess.run(
            ["cmake", "--build", str(self.cmake_debug)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False
        )
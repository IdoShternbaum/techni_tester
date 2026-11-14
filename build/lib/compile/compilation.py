import os
import subprocess
from configuration import Configure


class Compile(Configure):
    def __init__(self, project_path=None):
        super().__init__(project_path)
        self.result = self.compile()

    def compile(self):
        env = os.environ.copy()
        if self.compiler and self.compiler.is_file():
            env["PATH"] = str(self.compiler.parent) + os.pathsep + env.get("PATH", "")
        return subprocess.run(
            [str(self.cmake_command), "--build", str(self.cmake_debug)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            check=False
        )

import os
import subprocess
from pathlib import Path

from test_validation import TestValidator


def find_executable(build_dir, selected=None):
    if selected:
        executable = Path(selected).resolve()
        if not executable.is_file():
            raise FileNotFoundError(f"Executable not found: {executable}")
        return executable

    build_dir = Path(build_dir)
    if os.name == "nt":
        candidates = sorted(build_dir.glob("*.exe"))
    else:
        candidates = sorted(p for p in build_dir.iterdir() if p.is_file() and os.access(p, os.X_OK))
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one executable in {build_dir}, found {len(candidates)}. "
            "Specify one with --executable."
        )
    return candidates[0].resolve()


class TestRunner:
    def __init__(self, project_path, executable, timeout=5):
        self.project_path = Path(project_path)
        self.executable = Path(executable)
        self.timeout = timeout

    def run(self):
        validator = TestValidator(self.project_path)
        results = []
        for path in validator.find_test_files():
            for test in validator.read_test_file(path):
                results.append(self.run_test(test, path.name))
        return results

    def run_test(self, test, filename):
        result = {"name": test["name"], "file": filename, "expected": test["output"]}
        try:
            process = subprocess.run(
                [str(self.executable)], input=test["input"], capture_output=True,
                text=True, encoding="utf-8", errors="replace", cwd=self.project_path,
                timeout=self.timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            result.update(passed=False, reason=f"Timed out after {self.timeout} seconds")
            return result
        result.update(actual=process.stdout, stderr=process.stderr, returncode=process.returncode)
        result["passed"] = process.returncode == 0 and process.stdout == test["output"]
        return result

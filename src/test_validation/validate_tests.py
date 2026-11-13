import json
from pathlib import Path


class TestValidator:
    def __init__(self, project_path):
        self.tests_dir = Path(project_path) / "tests"

    def check(self):
        for path in self.find_test_files():
            tests = self.read_test_file(path)
            for index, test in enumerate(tests, start=1):
                self.validate_test(test, path, index)

    def find_test_files(self):
        if not self.tests_dir.is_dir():
            raise NotADirectoryError(f"Tests directory not found: {self.tests_dir}")

        json_files = sorted(self.tests_dir.glob("*.json"))
        if not json_files:
            raise FileNotFoundError(f"No JSON test files found in: {self.tests_dir}")
        return json_files

    @staticmethod
    def read_test_file(path):
        try:
            with path.open("r", encoding="utf-8-sig") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValueError(f"Invalid JSON in {path}: {error}") from error

        if not isinstance(data, dict) or not isinstance(data.get("tests"), list):
            raise ValueError(f"{path}: expected an object with a 'tests' array")
        return data["tests"]

    @staticmethod
    def validate_test(test, path, index):
        if not isinstance(test, dict):
            raise ValueError(f"{path}: test {index} must be an object")
        for field in ("name", "input", "output"):
            if not isinstance(test.get(field), str):
                raise ValueError(f"{path}: test {index} must have a string '{field}'")

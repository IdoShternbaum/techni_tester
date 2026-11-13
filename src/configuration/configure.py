import json
from typing import Any

from validation import Validate


class Configure(Validate):

    def __init__(self):
        super().__init__()

        self.check()
        self.commands = self.parse_json()

        self.command = self.commands.get("command")
        self.directory = self.commands.get("directory")

        if not self.can_compile():
            raise ValueError(
                "Configure error!\n"
                "Missing or invalid compiler command!\n"
            )

    def parse_json(self) -> dict:
        with self.cmpl_cmd_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        if isinstance(data, list) and data:
            return data[0]

        raise ValueError(
            "Configure error!\n"
            f"{self.cmpl_cmd_path} is not a valid config file!\n"
        )


    @staticmethod
    def is_valid(x:Any) -> bool:
        return isinstance(x, str) and bool(x.strip())

    def can_compile(self) -> bool:
        return self.is_valid(self.command) and self.is_valid(self.directory)
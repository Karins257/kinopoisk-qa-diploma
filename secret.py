"""Prevent credentials from appearing in pytest fixture representations."""


class ApiKey:
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return "ApiKey([REDACTED])"

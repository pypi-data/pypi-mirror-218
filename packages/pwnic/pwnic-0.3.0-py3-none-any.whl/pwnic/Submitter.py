from collections.abc import Iterable


class Submitter:
    def __init__(self) -> None:
        return

    def submit(self, flags: Iterable[str | bytes]) -> None:
        return

    def fetch_unsent(self) -> list[str]:
        return []

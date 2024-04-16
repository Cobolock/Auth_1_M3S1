from typing import Protocol


class DBSessionProtocol(Protocol):
    def add(self, model) -> None:
        """Add model to transaction"""

    async def commit(self) -> None:
        """Commit to database"""


class CacheSessionProtocol(Protocol):
    pass

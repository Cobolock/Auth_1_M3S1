from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from typing import Annotated
from auth.db.postgres import get_session
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from auth.core.exceptions import ObjectAlreadyExistsError
from auth.schemas.user import Entry


@dataclass
class EntryRepository:
    _session: Annotated[AsyncSession, Depends(get_session)]

    async def add(self, entry: Entry) -> Entry:
        self._session.add(entry)
        try:
            await self._session.commit()
        except IntegrityError:
            raise ObjectAlreadyExistsError(Entry) from None
        return entry

    async def get_all(self, user_id) -> list[Entry]:
        query = select(Entry).where(Entry.user_id == user_id)
        return list(await self._session.scalars(query))

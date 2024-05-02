from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.exceptions import ObjectAlreadyExistsError
from auth.db.postgres import get_session
from auth.models.entry import Entry as EntryModel


@dataclass
class EntryRepository:
    _session: Annotated[AsyncSession, Depends(get_session)]

    async def add(self, entry: EntryModel) -> EntryModel:
        self._session.add(entry)
        try:
            await self._session.commit()
        except IntegrityError:
            raise ObjectAlreadyExistsError(EntryModel) from None
        return entry

    async def get_last_10(self, user_id) -> list[EntryModel]:
        query = (
            select(EntryModel)
            .where(EntryModel.user_id == user_id)
            .order_by(EntryModel.created)
            .limit(10)
        )
        return list(await self._session.scalars(query))

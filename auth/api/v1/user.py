from typing import Annotated

from fastapi import APIRouter, Depends, status

from auth.models.entry import Entry
from auth.schemas.user import EntrySchema
from auth.services.user import UserService

router = APIRouter(tags=["Login History"])


@router.post("/entry", status_code=status.HTTP_201_CREATED)
async def add_entry(
    username: str, entry: EntrySchema, user_service: Annotated[UserService, Depends()]
) -> None:
    """Вносит запись о входе пользователя."""
    await user_service.add_entry(username, entry)


@router.get("/entries", status_code=status.HTTP_200_OK, response_model=list[EntrySchema])
async def get_entries(
    username: str, user_service: Annotated[UserService, Depends()]
) -> list[Entry]:
    """Выводит все записи о входах пользователя."""
    return await user_service.get_entries(username)

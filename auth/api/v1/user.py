

@router.post("/entry", status_code=HTTPStatus.OK)
async def add_entry(
    username: str, entry: EntrySchema, user_service: Annotated[UserService, Depends()]
) -> None:
    """Вносит запись о входе пользователя."""
    await user_service.add_entry(username, entry)


@router.get("/entries", status_code=HTTPStatus.OK, response_model=list[EntrySchema])
async def get_entries(
    username: str, user_service: Annotated[UserService, Depends()]
) -> list[EntryModel]:
    """Выводит все записи о входах пользователя."""
    return await user_service.get_entries(username)

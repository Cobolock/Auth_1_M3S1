from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from auth.models.social_account import SocialAccount
from auth.models.user import User
from auth.db.postgres import get_session
from auth.core.utils import generate_random_string


@dataclass
class SocialServiceRepository:
    _session: Annotated[AsyncSession, Depends(get_session)]

    async def get_user(
        self, social_id: str, social_name: str, username: str, first_name: str, last_name
    ) -> User:
        # Проверка наличия Аккаунта социальной сети у пользователя
        result = await self._session.execute(
            select(SocialAccount).where(
                SocialAccount.social_id == social_id, SocialAccount.social_name == social_name
            )
        )
        social_account = result.scalars().first()
        # Если аккаунт существует, то возвращаем его пользователя
        if social_account:
            result = await self._session.execute(
                select(User).where(User.id == social_account.user_id)
            )
            return result.scalars().first()

        # Если аккаунт не существует проверяем что проверяем наличие такого
        # пользователя
        result = await self._session.execute(select(User).where(User.username == username))
        user = result.scalars().first()

        # Если пользователя не существует, то создаем его, генерируя случайный пароль
        if not user:
            user = User(
                username=username,
                password=generate_random_string(),
                first_name=first_name,
                last_name=last_name,
            )
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)

        # Создаем его модель Аккаунта от социальной сети
        social_account = SocialAccount(
            user_id=user.id, social_id=social_id, social_name=social_name
        )
        self._session.add(social_account)
        await self._session.commit()

        return user

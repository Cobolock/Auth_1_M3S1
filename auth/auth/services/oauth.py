from typing import Annotated

from dataclasses import dataclass
import httpx
from fastapi import Depends, status

from auth.core.config import yandex_auth_settings
from auth.models.user import User
from auth.repositories.social_account import SocialServiceRepository
from auth.repositories.user import UserRepository


@dataclass
class YandexService:
    user_repo: Annotated[UserRepository, Depends()]
    social_account_repo: Annotated[SocialServiceRepository, Depends()]
    http_client = httpx.AsyncClient()

    # Делаем попытку получить токен пользователя по его коду подтверждения
    async def get_user(self, code) -> User | None:
        try:
            response = await self.http_client.post(
                url="https://oauth.yandex.ru/token",
                data={
                    "code": code,
                    "grant_type": "authorization_code",
                    "client_id": yandex_auth_settings.yandex_client_id,
                    "client_secret": yandex_auth_settings.yandex_client_secret,
                },
            )
            if response.status_code != status.HTTP_200_OK:
                return None

            data = response.json()
            access_token = data.get("access_token")

            # Делаем попытку получить данные пользователя у Яндекса по его
            # токену доступа
            user_info_response = await self.http_client.get(
                url="https://login.yandex.ru/info",
                headers={"Authorization": f"OAuth {access_token}"},
            )
            if user_info_response.status_code != status.HTTP_200_OK:
                return None

            user_data = user_info_response.json()

        except httpx.HTTPError:
            return None
        # В случае успешного выполнения запросов вызываем репозиторий и создаем
        # модели пользователя
        return await self.social_account_repo.get_user(
            social_id=user_data.get("psuid"),
            social_name="yandex",
            username=user_data.get("display_name"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
        )

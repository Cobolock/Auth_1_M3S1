from typing import Any

from fastapi import HTTPException, status


class ApplicationError(HTTPException):
    """Базовый класс для ошибок приложения.

    Используется для наследования более конкретных ошибок,
    которые FastAPI умеет сериализовывать.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    headers: dict[Any, Any] | None = None
    detail: str = "Произошла ошибка приложения"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "status_code" not in kwargs:
            kwargs["status_code"] = self.status_code
        if "detail" not in kwargs:
            kwargs["detail"] = str(self.detail)
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers

        super().__init__(*args, **kwargs)


class ObjectAlreadyExistsError(ApplicationError):
    """Объект уже существует в базе данных."""

    status_code = status.HTTP_409_CONFLICT

    def __init__(self, obj_class: type | None) -> None:
        obj_name = obj_class.__name__ if obj_class is not None else "Object"
        super().__init__(detail=f"{obj_name} already exists")


class ObjectNotFoundError(ApplicationError):
    """Объект не найден в базе данных."""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, obj_class: type | None) -> None:
        obj_name = obj_class.__name__ if obj_class is not None else "Object"
        super().__init__(detail=f"{obj_name} not found")


class RoleDeletionProhibitedError(ApplicationError):
    """Роль нельзя удалить."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Role deletion prohibited"


class NotAuthorizedError(ApplicationError):
    """Пользователь не авторизован."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"


class BadRefreshTokenError(ApplicationError):
    """Refresh Token устарел или не существует."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Your refresh token void"


class TokenMalformedError(ApplicationError):
    """Токен был изменён."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Your refresh token is malformed"


class UsernameInUseError(ApplicationError):
    """Пользователь с таким именем уже существует."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Username in use"

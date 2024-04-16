from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from auth.db.redis import get_redis
from auth.db.postgres import get_session
from auth.models.user import User
from auth.schemas.common import DBSessionProtocol, CacheSessionProtocol


class UserService:
    def __init__(self, db_session: DBSessionProtocol, cache_session: CacheSessionProtocol) -> None:
        self.db_session = db_session
        self.cache_session = cache_session

    async def create(self, username, password) -> bool:
        new_user = User(username, password)
        self.db_session.add(new_user)
        try:
            await self.db_session.commit()
            return True
        except IntegrityError:
            return False
        except:
            raise


async def get_user_service(
    db_session: AsyncSession = Depends(get_session), cache_session: Redis = Depends(get_redis)
) -> UserService:
    return UserService(db_session, cache_session)

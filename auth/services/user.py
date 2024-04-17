from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from auth.db.redis import get_redis
from auth.db.postgres import get_session
from auth.models.user import User
from auth.schemas.common import DBSessionProtocol, CacheSessionProtocol
from auth.schemas.user import Credentials


class UserService:
    def __init__(self, db_session: DBSessionProtocol, cache_session: CacheSessionProtocol) -> None:
        self.db_session = db_session
        self.cache_session = cache_session

    async def create(self, creds: Credentials) -> bool:
        new_user = User(creds.username, creds.password)
        self.db_session.add(new_user)
        try:
            await self.db_session.commit()
            return True
        except IntegrityError:
            return False
        except:
            raise

    async def get(self, username: str) -> User:
        query = select(User).where(User.username == username)
        if user_rows := await self.db_session.execute(query):
            user = user_rows.scalar()
            return user

    async def check_creds(self, creds: Credentials) -> bool:
        if user := await self.get(creds.username):
            return user.check_password(creds.password)


async def get_user_service(
    db_session: AsyncSession = Depends(get_session), cache_session: Redis = Depends(get_redis)
) -> UserService:
    return UserService(db_session, cache_session)

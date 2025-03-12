from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import create_model

from app.dao.session_maker import connection
from app.dao.base import BaseDAO
from app.models.user import User
from app.schemas.user import UserData, UserLogin, FindUser, UserCreate


class UserDAO(BaseDAO[User]):
    model = User

    @connection
    async def find_user(user_data: FindUser, session: AsyncSession) -> UserData:

        result = await UserDAO.find_one_or_none(session=session, filters=user_data)

        return result

    @connection
    async def find_user_by_id(user_id: int, session: AsyncSession) -> UserData:

        result = await UserDAO.find_one_or_none_by_id(session=session, id=user_id)

        return result

    @connection
    async def find_all_users(session: AsyncSession) -> list[UserData]:
        return await UserDAO.find_all(session=session)

    @connection
    async def add_user(user_data: dict, session: AsyncSession) -> UserData:
        new_user = await UserDAO.add(session=session, values=UserCreate(**user_data))

        return new_user

    @connection
    async def delete_user_by_id(user_id: int, session: AsyncSession):
        await UserDAO.delete_one_by_id(session=session, id=user_id)

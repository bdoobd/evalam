from sqlalchemy.ext.asyncio import AsyncSession

from app.db_base import connection
from app.dao.base import BaseDAO
from app.models.user import User
from app.schemas.user import UserData


class UserDAO(BaseDAO):
    model = User

    @connection
    async def add_user(user_data: dict, session: AsyncSession) -> UserData:

        new_user = await UserDAO.add(session=session, **user_data)

        return new_user

    @connection
    async def find_user(filter: dict, session: AsyncSession) -> UserData:
        result = await UserDAO.find_one_or_none(session=session, **filter)

        return result

    @connection
    async def find_all_users(session: AsyncSession) -> list[UserData]:
        return await UserDAO.find_all(session=session)

    @connection
    async def delete_user_by_id(user_id: int, session: AsyncSession):
        await UserDAO.delete_one_by_id(session=session, id=user_id)

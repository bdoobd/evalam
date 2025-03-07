from sqlalchemy.ext.asyncio import AsyncSession

from app.db_base import connection
from app.dao.base import BaseDAO
from app.models.user import User


class UserDAO(BaseDAO):
    model = User

    @connection
    async def add_user(user_data, session: AsyncSession):

        new_user = await UserDAO.add(session=session, **user_data)

        return new_user

    @connection
    async def find_user(filter, session: AsyncSession):
        result = await UserDAO.find_one_or_none(session=session, **filter)

        return result

    @connection
    async def find_all_users(session: AsyncSession):
        return await UserDAO.find_all(session=session)

from app.dao.db_base import async_session_maker


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, **kwargs, session=session)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper

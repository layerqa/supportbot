from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    full_name: str,
    username: str | None,
) -> tuple[User, bool]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if user is not None:
        return user, False

    user = User(telegram_id=telegram_id, full_name=full_name, username=username)
    session.add(user)
    await session.flush()
    return user, True


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    return await session.scalar(select(User).where(User.telegram_id == telegram_id))


async def ban_user(session: AsyncSession, telegram_id: int) -> User:
    user = await get_user_by_telegram_id(session, telegram_id)
    if user is None:
        raise ValueError(f"User {telegram_id} not found")

    user.is_banned = True
    await session.flush()
    return user


async def set_locale(session: AsyncSession, user: User, locale: str) -> None:
    user.locale = locale
    await session.flush()

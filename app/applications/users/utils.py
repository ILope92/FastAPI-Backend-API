from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.users.models import User


async def update_last_login(db_session: AsyncSession, user_id: int) -> None:
    user = await User.get_user_for_id(db_session=db_session, user_id=user_id)
    user.last_login = datetime.utcnow()
    await user.save(db_session=db_session)

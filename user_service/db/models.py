from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.db.engine import Base, metadata


class User(Base):
    __tablename__ = "user"
    __metadata__ = metadata
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(cls)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_user(cls, session: AsyncSession, user_id: int):
        query = select(cls).where(cls.id == user_id)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def create_user(cls, session: AsyncSession, data: dict):
        user = cls(
            name=data.get("name"),
            surname=data.get("surname"),
            password=data.get("password"),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @classmethod
    async def update_user(cls, session: AsyncSession, user_id: int, data: dict):
        query = (
            update(cls)
            .where(cls.id == user_id)
            .values(**data)
            .returning(cls)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalar()

    @classmethod
    async def delete_user(cls, session: AsyncSession, user_id: int):
        query = delete(cls).where(cls.id == user_id)
        await session.execute(query)
        await session.commit()

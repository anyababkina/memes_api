from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Memes
from src.helpers import NotFoundError
from src.schemas import CreateMemSchema


class MemesQueryset:
    model = Memes

    @classmethod
    async def create(cls, schema: CreateMemSchema, session: AsyncSession) -> Memes:
        data = schema.model_dump()
        instance = cls.model(**data)

        session.add(instance)
        await session.flush()

        return instance

    @classmethod
    async def get_by_id(cls, instance_id: int, session: AsyncSession) -> Memes | None:
        instance = await session.get(cls.model, instance_id)

        return instance

    @classmethod
    async def get_multiple(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)

        return result.scalars().unique().all()

    @classmethod
    async def delete(cls, instance_id: int, session: AsyncSession) -> None:
        """"
        Delete instance in db and return image_name to delete image in S3
        """

        instance = await cls.get_by_id(instance_id, session)
        if instance is None:
            raise NotFoundError

        await session.delete(instance)
        await session.flush()

        return

    @classmethod
    async def update(cls, instance_id: int, schema: CreateMemSchema, session: AsyncSession) -> Memes:
        instance = await cls.get_by_id(instance_id, session)
        if instance is None:
            raise NotFoundError

        data = schema.model_dump(exclude_none=True, exclude_unset=True)
        for key, value in data.items():
            setattr(instance, key, value)

        session.add(instance)
        await session.flush()

        return instance

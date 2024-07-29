from typing import Annotated, Optional

from fastapi import APIRouter, UploadFile, File, Depends
from starlette import status

from src.helpers import AsyncSessionMakerDep
from src.schemas import MemesSchema, CreateMemSchema
from src.services import get_mem_service, get_memes_service, get_mem_photo_service, create_mem_service, \
    delete_mem_service, update_mem_service

router = APIRouter(
    prefix='/memes',
    tags=['Public API memes'],
)


@router.get('/{mem_id}', response_model=MemesSchema)
async def get_mem(
        mem_id: int,
        session_maker: AsyncSessionMakerDep
):
    """"
    Return mem info
    """

    result = await get_mem_service(
        mem_id=mem_id,
        session_maker=session_maker
    )

    return result


@router.get('', response_model=list[MemesSchema])
async def get_memes(
        session_maker: AsyncSessionMakerDep
):
    result = await get_memes_service(
        session_maker=session_maker
    )

    return result


@router.get('/{mem_id}/photo')
async def get_mem_photo(
        mem_id: int,
        session_maker: AsyncSessionMakerDep
):
    """"
    Get mem image using mem_id
    """

    result = await get_mem_photo_service(
        mem_id=mem_id,
        session_maker=session_maker
    )

    return result


@router.post('', response_model=MemesSchema, status_code=status.HTTP_201_CREATED)
async def create_mem(
        session_maker: AsyncSessionMakerDep,
        schema: Annotated[CreateMemSchema, Depends(CreateMemSchema.as_form)],
        file: UploadFile = File(...)
):
    result = await create_mem_service(
        schema=schema,
        file=file,
        session_maker=session_maker
    )

    return result


@router.delete('/{mem_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_mem(
        mem_id: int,
        session_maker: AsyncSessionMakerDep
):
    await delete_mem_service(
        mem_id=mem_id,
        session_maker=session_maker
    )

    return


@router.put('/{mem_id}', response_model=MemesSchema)
async def update_mem(
        mem_id: int,
        session_maker: AsyncSessionMakerDep,
        schema: Annotated[CreateMemSchema, Depends(CreateMemSchema.as_form)],
        file: Optional[UploadFile] = File(None)

):
    result = await update_mem_service(
        mem_id=mem_id,
        schema=schema,
        file=file,
        session_maker=session_maker
    )

    return result
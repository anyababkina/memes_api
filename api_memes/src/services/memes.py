import os
import tempfile

import aiohttp
from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from starlette import status
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.cruds import MemesQueryset
from src.helpers import NotFoundError
from src.schemas import MemesSchema, CreateMemSchema
from src.settings import env_settings


async def get_mem_service(
        mem_id: int,
        session_maker: async_sessionmaker
):
    async with session_maker.begin() as session:
        instance_mem = await MemesQueryset.get_by_id(mem_id, session)

        if instance_mem is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mem isn't found")

        result = MemesSchema.model_validate(instance_mem)

    return result


async def get_memes_service(
        session_maker: async_sessionmaker
):
    async with session_maker.begin() as session:
        memes = await MemesQueryset.get_multiple(session)
        result = [MemesSchema.model_validate(mem) for mem in memes]

    return result


async def get_mem_photo_service(
        mem_id: int,
        session_maker: async_sessionmaker
):
    async with session_maker.begin() as session:
        instance_mem = await MemesQueryset.get_by_id(mem_id, session)
        if instance_mem is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mem isn't found")

        # отправляю в хранилище запрос на скачивание файла
        url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file/{mem_id}'
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file_path = temp_file.name
            async with aiohttp.ClientSession() as request_session:
                async with request_session.get(url) as response:
                    if response.status != 200:
                        if response.status == 404:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
                        else:
                            raise HTTPException(status_code=response.status, detail='Something went wrong in S3 server')

                    # Записываем данные в файл
                    with open(temp_file_path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)

            def file_iterator(file_path):
                with open(file_path, "rb") as file:
                    yield from file
                # Удаляем временный файл после завершения передачи данных
                os.remove(file_path)

            headers = {'Content-Disposition': f'inline; filename="{mem_id}.png"'}
            return StreamingResponse(
                file_iterator(temp_file_path),
                media_type='application/octet-stream',
                headers=headers
            )


async def create_mem_service(
        schema: CreateMemSchema,
        file: UploadFile,
        session_maker: async_sessionmaker
):
    async with session_maker.begin() as session:
        instance_mem = await MemesQueryset.create(schema, session)

        # отправляю в хранилище запрос на создание файла
        url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file'
        async with aiohttp.ClientSession() as request_session:
            form_data = aiohttp.FormData()
            form_data.add_field('mem_id', str(instance_mem.id))
            file_content = await file.read()
            form_data.add_field('file', file_content, filename=file.filename, content_type=file.content_type)

            async with request_session.post(url, data=form_data) as response:
                if response.status != 201:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Something went wrong in S3 server'
                    )

        result = MemesSchema.model_validate(instance_mem)

    return result


async def delete_mem_service(
        mem_id: int,
        session_maker: async_sessionmaker
):
    async with session_maker.begin() as session:
        try:
            await MemesQueryset.delete(mem_id, session)

            # отправляем запрос на удаление файла в s3
            url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file/{mem_id}'
            async with aiohttp.ClientSession() as request_session:
                async with request_session.delete(url) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail='Something went wrong in S3 server')

        except NotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mem isn't found")

    return


async def update_mem_service(
        mem_id: int,
        schema: CreateMemSchema,
        file: UploadFile | None,
        session_maker: async_sessionmaker
):
    try:
        async with session_maker.begin() as session:
            instance_mem = await MemesQueryset.update(mem_id, schema, session)
            if file:
                # отправляем запрос в s3 на удаление существующего и добавление нового
                url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file'
                async with aiohttp.ClientSession() as request_session:
                    form_data = aiohttp.FormData()
                    form_data.add_field('mem_id', str(instance_mem.id))
                    file_content = await file.read()
                    form_data.add_field('file', file_content, filename=file.filename, content_type=file.content_type)

                    async with request_session.post(url, data=form_data) as response:
                        if response.status != 201:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Something went wrong in S3 server'
                            )

            result = MemesSchema.model_validate(instance_mem)

        return result

    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mem isn't found")

import os
import tempfile

from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from starlette import status

from src.helpers import S3FileManager
from src.helpers.exceptions import S3Error


async def create_file_service(
        mem_id: int,
        file: UploadFile
):
    try:
        file_content = await file.read()
        object_key = f'{mem_id}.png'
        file_url = S3FileManager.upload_file(file_content, object_key)
        return {"message": f"Successfully uploaded {file.filename} to S3", "url": file_url}

    except S3Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong in S3 server')


def get_file_service(
        mem_id: int
):
    try:
        object_key = f'{mem_id}.png'
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as file:
            temp_file_name = file.name
            S3FileManager.download_file(object_key, temp_file_name)

        def file_iterator(file_path):
            with open(file_path, "rb") as file:
                yield from file
            # Удаляем временный файл после завершения передачи данных
            os.remove(file_path)

        headers = {'Content-Disposition': f'attachment; filename="{object_key}"'}
        return StreamingResponse(
            file_iterator(temp_file_name),
            media_type='application/octet-stream',
            headers=headers
        )

    except HTTPException as e:
        raise e

    except S3Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong in S3 server')


def delete_file_service(
        mem_id: int
):
    try:
        object_key = f'{mem_id}.png'
        S3FileManager.delete_file(object_key)
        return {"message": f"Successfully deleted {object_key} from S3"}

    except S3Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong in S3 server')



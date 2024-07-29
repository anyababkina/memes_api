from typing import Annotated

from fastapi import APIRouter, Body, UploadFile, File
from starlette import status

from src.services import create_file_service, get_file_service, delete_file_service
from src.settings.swagger_doc import example_responses_get, example_responses_delete, example_responses_create

router = APIRouter(
    prefix='/s3',
    tags=['S3 communication']
)


@router.post('/file', status_code=status.HTTP_201_CREATED, responses=example_responses_create)
async def create_file(
        mem_id: Annotated[int, Body(embed=True)],
        file: Annotated[UploadFile, File(...)]
):
    """"
    Upload file in S3 storage. We will use mem_id as name for file in storage.
    You can use it for creating new mem and upload image for old one, because S3 rewrite file with same name
    """

    result = await create_file_service(
        mem_id=mem_id,
        file=file
    )

    return result


@router.get('/file/{mem_id}', responses=example_responses_get)
def get_file(
        mem_id: int
):
    """"
    Download file from S3. Give mem_id for downloading current file from storage. Return StreamingResponse
    """

    result = get_file_service(
        mem_id=mem_id
    )

    return result


@router.delete('/file/{mem_id}', responses=example_responses_delete)
def delete_file(
        mem_id: int
):
    """"
    Delete file from S3. Give mem_id for this
    """

    result = delete_file_service(
        mem_id=mem_id
    )

    return result
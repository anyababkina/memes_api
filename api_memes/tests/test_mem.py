import os
import tempfile

from aioresponses import aioresponses

from src.settings import env_settings
from tests.conftest import prefix

# создание мема - запись в бд, 201
# создание мема - ошибка на стороне сервера с S3 - 400
# получить один мем - чтение из бд
# получить один мем, несуществующий id - 404
# получить все мемы
# обновить мем
# обновить несуществующий - 404
# удалить мем - 204
# удалить несуществующий - 404


# создание мема - запись в бд, 201
async def test_create_mem(
        ac
):
    url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file'
    mock_response_json = {"message": f"Successfully uploaded to S3", "url": 'test_url'}

    with aioresponses() as m:
        m.post(url, status=201, payload=mock_response_json)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(b'testtestdatafile')

        response = await ac.post(
            prefix.PREFIX_MEM,
            data={'description': 'blabla'},
            files={'file': open(temp_file.name, 'rb')},
        )
        os.unlink(temp_file.name)

        assert response.status_code == 201
        assert response.json() == {'id': 2, 'description': 'blabla'}


# создание мема - ошибка на стороне сервера с S3 - 400
async def test_create_mem_error_in_S3_service(
        ac
):
    url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file'
    mock_response_json = {"message": 'any error'}

    with aioresponses() as m:
        m.post(url, status=403, payload=mock_response_json)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(b'testtestdatafile')

        response = await ac.post(
            prefix.PREFIX_MEM,
            data={'description': 'blabla'},
            files={'file': open(temp_file.name, 'rb')},
        )
        os.unlink(temp_file.name)

        assert response.status_code == 400
        assert response.json() == {'detail': 'Something went wrong in S3 server'}


# получить один мем - чтение из бд
async def test_get_mem(
        ac
):
    response = await ac.get(
        f'{prefix.PREFIX_MEM}/1'
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'description': 'test1'
    }


# получить один мем, несуществующий id - 404
async def test_get_mem_wrong_id(
        ac
):
    response = await ac.get(
        f'{prefix.PREFIX_MEM}/10'
    )

    assert response.status_code == 404
    assert response.json() == {'detail': "Mem isn't found"}


# получить все мемы
async def test_get_memes(
        ac
):
    response = await ac.get(
        prefix.PREFIX_MEM
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 1,
            'description': 'test1'
        }
    ]


# обновить мем
async def test_update_mem(
        ac
):
    response = await ac.put(
        f'{prefix.PREFIX_MEM}/1',
        data={'description': 'another blablabla'}
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'description': 'another blablabla'
    }


# обновить несуществующий - 404
async def test_update_mem_wrong_id(
        ac
):
    response = await ac.put(
        f'{prefix.PREFIX_MEM}/10',
        data={'description': 'another blablabla'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': "Mem isn't found"}


# удалить мем - 204
async def test_delete_mem(
        ac
):
    url = f'http://{env_settings.S3_API_HOST}:{env_settings.S3_API_PORT}/s3/file/1'
    mock_response_json = {"message": f"Successfully deleted from S3"}

    with aioresponses() as m:
        m.delete(url, status=200, payload=mock_response_json)
        response = await ac.delete(
            f'{prefix.PREFIX_MEM}/1',
        )

        assert response.status_code == 204


# удалить несуществующий - 404
async def test_delete_mem_wrong_id(
        ac
):
    response = await ac.delete(
        f'{prefix.PREFIX_MEM}/10',
    )

    assert response.status_code == 404
    assert response.json() == {'detail': "Mem isn't found"}
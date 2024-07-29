import pytest
from httpx import AsyncClient, ASGITransport
from pydantic_settings import BaseSettings
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core import utils
from testcontainers.postgres import PostgresContainer

from src.database.models import Memes
from src.database.models.base import Base
from src.helpers.dependencies import get_session_maker
from src.main import app
from src.settings import test_settings


class CustomPostgresContainer(PostgresContainer):
    def __init__(self,
                 image="postgres:latest",
                 port=5432, username=None,
                 password=None,
                 dbname=None,
                 driver="psycopg2",
                 **kwargs):
        super(PostgresContainer, self).__init__(image=image, **kwargs)
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = port
        self.driver = driver
        self.with_exposed_ports(self.port)

    def get_connection_url(self, host=None, *args, **kwargs):
        return super()._create_connection_url(dialect="postgresql+{}".format(self.driver),
                                              username=self.username,
                                              password=self.password,
                                              dbname=self.dbname,
                                              host=host,
                                              port=self.port)


@pytest.fixture(scope="session")
async def postgres_container() -> CustomPostgresContainer:

    """ Тест контейнер """

    postgres = CustomPostgresContainer(
        image=test_settings.TEST_POSTGRES_IMAGE,
        username=test_settings.TEST_POSTGRES_USER,
        password=test_settings.TEST_POSTGRES_PASSWORD,
        dbname=test_settings.TEST_POSTGRES_DATABASE,
        port=test_settings.TEST_POSTGRES_CONTAINER_PORT,
        driver='asyncpg'
    )
    with postgres:
        postgres.driver = "asyncpg"
        wait_for_logs(
            postgres,
            r"UTC \[1\] LOG:  database system is ready to accept connections",
            10,
        )
        yield postgres


@pytest.fixture(scope="function", autouse=True)
async def prepare_db_and_session(postgres_container: PostgresContainer) -> async_sessionmaker:

    """" Соединение с тест контейнером бд, создание таблиц, создание данных в таблицах для тестов. Получение сессии. """

    if utils.is_windows():
        postgres_container.get_container_host_ip = lambda: "localhost"
    url = postgres_container.get_connection_url()
    engine = create_async_engine(url)

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

        await connect.execute(
            insert(Memes),
            [
                {
                    'description': 'test1'
                }
            ]
        )

    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    yield async_session_maker

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def override(prepare_db_and_session):
    app.dependency_overrides[get_session_maker] = lambda: prepare_db_and_session
    print('override')
    yield
    app.dependency_overrides.clear()
    print('stop')


@pytest.fixture()
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


class TestPrefixSettings(BaseSettings):
    PREFIX_MEM: str = "memes"


prefix = TestPrefixSettings()
import pytest
from unittest.mock import AsyncMock, MagicMock
from unittest import mock
from bson import ObjectId

from domain.repository.client import ClientRepository
from domain.models.repository.output import ClientModel
from domain.models.enums import AccountStatus, ClientStatus
from adapters.database.async_mongo import DatabaseClient

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def client_repository(mongo_mock, mock_logger):
    return ClientRepository(mongo_mock, mock_logger)

@pytest.fixture(scope="function")
def mongo_mock():
    return DatabaseClient("mockDB", mock.Mock(), "http://mock_url")


@pytest.mark.asyncio
async def test_get_client_by_query(client_repository, mongo_mock):

    mock_data = ClientModel(name="Test Client", device_id="device123", device_type="typeA", status=AccountStatus.ACTIVE)
    await mongo_mock.create("mockDB", mock_data.model_dump(by_alias=True))
    result = await client_repository.get_client_by_query()

    assert len(result) == 1
    assert isinstance(result[0], ClientModel)

@pytest.fixture
def random_objectid():
    return ObjectId()

@pytest.mark.asyncio
async def test_update_client(client_repository, mongo_mock, random_objectid):

    client_id = str(random_objectid)
    update_data = {"status": AccountStatus.INACTIVE}
    mock_data = {
        "client_id": client_id,  
        "device_id": "device123", 
        "device_type": "typeA", 
        "status": AccountStatus.ACTIVE
    }
    collection_mock = AsyncMock()
    collection_mock.update_one = AsyncMock(return_value=AsyncMock(matched_count=1))
    collection_mock.find_one = AsyncMock(return_value=mock_data)
    mongo_mock.get_collection = MagicMock(return_value=collection_mock)
    client_repository._database.update = AsyncMock(return_value=mock_data)
    result = await client_repository.update_client(update_data, client_id)

    assert result.id == ObjectId(client_id)
    assert result.device_id == "device123"
    assert result.device_type == "typeA"
    assert result.status == AccountStatus.ACTIVE
    client_repository._database.update.assert_called_once()

@pytest.mark.asyncio
async def test_create_client(client_repository, mongo_mock, random_objectid):

    client_id = str(random_objectid)
    mock_data = ClientModel(
        id=client_id,
        name="Test Client",
        device_id="device123", 
        device_type="typeA", 
        status=AccountStatus.ACTIVE)


    collection_mock = AsyncMock()
    collection_mock.insert_one = AsyncMock(return_value=AsyncMock(inserted_id=client_id))
    mongo_mock.get_collection = MagicMock(return_value=collection_mock)
    client_repository._database.create = AsyncMock(return_value=mock_data)
    result = await client_repository.create_client(mock_data)

    assert result.id == ObjectId(client_id)
    assert result.device_id == "device123"  # Verifica o valor correto do mock
    assert result.device_type == "typeA"
    assert result.status == AccountStatus.ACTIVE
    client_repository._database.create.assert_called_once()

@pytest.mark.asyncio
async def test_delete_client(client_repository, mongo_mock, random_objectid):

    client_data = {"_id": random_objectid}

    mongo_mock.delete = AsyncMock(return_value=None)
    await client_repository.delete_client(client_data)
    mongo_mock.delete.assert_called_once_with('account_requests', client_data)

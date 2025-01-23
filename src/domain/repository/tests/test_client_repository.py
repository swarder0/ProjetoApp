import pytest
from unittest.mock import AsyncMock, MagicMock
from unittest import mock
from bson import ObjectId

from domain.repository.client import ClientRepository
from domain.models.repository.output import ClientModel
from domain.models.enums import AccountStatus, ClientStatus
from adapters.database.async_mongo import DatabaseClient

@pytest.fixture
def mock_database_client():
    return AsyncMock()

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
    # Mock data
    mock_data = ClientModel(name="Test Client", device_id="device123", device_type="typeA", status=AccountStatus.ACTIVE)
    await mongo_mock.create("mockDB", mock_data.model_dump(by_alias=True))

    # Call method
    result = await client_repository.get_client_by_query()

    # Assertions
    assert len(result) == 1
    assert isinstance(result[0], ClientModel)

# @pytest.mark.asyncio
# async def test_update_client(client_repository, mock_database_client, random_objectid):
#     # Mock data
#     client_id = random_objectid
#     update_data = {"name": "Updated Client"}
#     mock_data = {"client_id": client_id, "name": "Updated Client", "device_id": "device123", "device_type": "typeA", "status": AccountStatus.ACTIVE}
#     mock_database_client.update.return_value = mock_data

#     # Call method
#     result = await client_repository.update_client(update_data, client_id)

#     # Assertions
#     assert result.name == "Updated Client"

# @pytest.mark.asyncio
# async def test_create_client(client_repository, mock_database_client):
#     # Mock data
#     client_data = {"client_id": "123", "name": "New Client", "device_id": "device123", "device_type": "typeA", "status": AccountStatus.ACTIVE}
#     mock_database_client.create.return_value = client_data

#     # Call method
#     result = await client_repository.create_client(client_data)

#     # Assertions
#     assert isinstance(result, ClientModel)
#     assert result.client_id == "123"
#     assert result.name == "New Client"

# @pytest.mark.asyncio
# async def test_delete_client(client_repository, mock_database_client, mock_logger, random_objectid):
#     # Mock data
#     client_data = {"_id": random_objectid, "status": ClientStatus.PENDING}
#     mock_database_client.delete.return_value = None

#     # Call method
#     await client_repository.delete_client(client_data)
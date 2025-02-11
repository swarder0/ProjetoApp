from typing import Optional

from bson import ObjectId

from src.domain.exceptions.exceptions import ClientNotFoundException
from src.domain.models.repository.output import ClientModel
from src.domain.models.enums import StepNames, ClientStatus
from src.adapters.database.async_mongo import DatabaseClient

class ClientRepository:
    def __init__(self, database_client: DatabaseClient, logger) -> None:
        self._database = database_client
        self.logger = logger

    async def get_client_by_query(self, query: Optional[dict] = None) -> list[ClientModel]:
        default_query = {}
        

        cursor = self._database.get_all("mockDB", default_query)
        print(cursor)
        cursor.sort("created_at", -1)
        return [ClientModel(**client) async for client in cursor]

    async def get_client_by_name(self, name: str) -> ClientModel:
        cursor = await self._database.get_all("account_requests", {"client.name": name})
        cursor.sort("created_at", -1) # type: ignore
        client = await cursor.to_list(length=1)
        if not client:
            raise ClientNotFoundException({"name": name})

        return ClientModel(**client[0])

    async def get_clients_by_client_ids(self, client_ids: list[str]) -> dict:
        query = {"client_id": {"$in": client_ids}}
        return await self.get_client_by_query(query)
    
    async def get_client_to_archived(self) -> list[ClientModel]:
        query = {"status": {"$in": [ClientStatus.PENDING, ClientStatus.FAILED]}}
        return await self.get_client_by_query(query)
    
    async def update_client(self, update_data: dict, client_id: str) ->ClientModel:
        client = await self._database.update("account_requests", {"_id": ObjectId(client_id)}, update=update_data)
        return ClientModel(**client)
    
    async def create_client(self, client_data: dict) -> ClientModel:
        return await self._database.create("account_requests", client_data)
    
    async def delete_client(self, client_data: dict | None):
        if client_data and client_data.get("status") != ClientStatus.COMPLETED:
            try:
                await self._database.delete("account_requests", {"_id": ObjectId(client_data.get("_id"))})
            except Exception as e:
                self.logger.error(f"Error deleting client: {e}")
                raise e


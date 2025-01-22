from motor.motor_asyncio import AsyncIOMotorClient
import logging
import sys
import traceback
from typing import Optional
from adapters.database.database_interfaces import DatabaseClientInterface
from pymongo import ReturnDocument

class DatabaseClient(DatabaseClientInterface):
    def __init__(self, Client_accounts: str, logger: logging.Logger, uri: str):
        self.logger = logger
        try:
            self._client = AsyncIOMotorClient(uri)
            self.database = self._client[Client_accounts]
            self.logger.info("Connected to MongoDB")
        except Exception as e:
            self.logger.error(f"Error connecting to MongoDB: {e}")
            raise self.DatabaseClientException(f"Error connecting to MongoDB: {e}")
    
    async def ping(self):
        return await self._client.admin.command("ping")

    async def create(self, collection: str, item: dict):
        try:
            result = await self.database[collection].insert_one(item)
            return result.inserted_id
        except Exception as err:
            self.logger.error(traceback.format_exc())
            raise err
        
    async def create_many(self, colletion: str, items: list[dict]):
        try:
            result = await self.database[colletion].insert_many(items)
            return result.inserted_ids
        except Exception as err:
            self.logger.error(traceback.format_exc())
            raise err
    
    def update(self, collection: str, query, update):
        return self.database[collection].find_one_and_update(
            filter=query, update=update, return_document=ReturnDocument.AFTER
        )
    
    async def get_one(self, collection: str, query, fields: Optional[dict] = None):
        if not fields:
            fields = {}
        return await self.database[collection].find_one(query, fields)
    
    def get_all(self, collection, *args, **kwargs):
        return self.database[collection].find(*args, **kwargs)
    
    async def delete(self, collection: str, query):
        return await self.database[collection].delete_many(query)
import logging
from typing import Any, Optional
import time

from src.domain.repository.client import ClientRepository
from src.adapters.database.async_mongo import DatabaseClient
from src.domain.services.client_service import ClientService
from src.adapters.cache.cache_interfaces import CacheInterface

class InMemoryCache(CacheInterface):
    def __init__(self):
        self.cache = {}
        self.ttl = {}  # Armazena os tempos de expiração
        self.logger = logging.getLogger(__name__)

    async def set_item(self, key: str, value: Any, ttl: Optional[int] = 60):
        self.cache[key] = value
        if ttl:
            self.ttl[key] = time.time() + ttl  # Tempo de expiração em segundos

    async def get_item(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if key in self.ttl and time.time() > self.ttl[key]:
                self.logger.info(f"Item expirado na cache: {key}")
                await self.delete_item(key)
                return None
            return self.cache[key]
        return None

    async def delete_item(self, key: str):
        if key in self.cache:
            del self.cache[key]
        if key in self.ttl:
            del self.ttl[key]

    async def get_all_items(self):
        return self.cache

    async def empty(self):
        self.cache.clear()
        self.ttl.clear()

    async def add_item(self, key: str, value: Any):
        if key not in self.cache:
            await self.set_item(key, value)

    async def exists(self, key: str) -> bool:
        return key in self.cache

    async def ping(self):
        return True

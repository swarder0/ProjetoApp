from contextlib import suppress
import logging
from typing import Optional

from src.adapters.cache.cache_interfaces import CacheInterface
from src.domain.exceptions.exceptions import ClientNotFoundException
from src.domain.models.repository.output import ClientModel
from src.domain.repository.client import ClientRepository
class ClientService:
    def __init__(
        self,
        cache: CacheInterface,
        logger: logging.Logger,
        client_repository: ClientRepository,
    ):
        self.logger = logger
        self.cache = cache
        self.client_repository = client_repository
    
    async def get_client_by_hash(self, x_client_hash: str)-> Optional[ClientModel]:
        client = None
        with suppress(ClientNotFoundException):
            name = self.get_name_by_hash(x_client_hash)
            client = await self.client_repository.get_client_by_name(name)
        return client
    
    async def get_name_by_hash(self, x_client_hash: str) -> str:
        self.logger.debug(f"Getting name by hash {x_client_hash=} from cache")
        name = await self.cache.get_item(f"client: {x_client_hash}")
        if not name:
            self.logger.debug(f"Hash {x_client_hash=} not found in cache, getting it from client_repository")
            client_hash = await self.client_repository.get_hash(key=x_client_hash)
            name = client_hash.name
            await self.cache.set_item(f"client: {x_client_hash}", name)
        return name
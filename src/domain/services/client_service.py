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
            name = await self.get_name_by_hash(x_client_hash)
            client = await self.client_repository.get_client_by_name(name)
        return client
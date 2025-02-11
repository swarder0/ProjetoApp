import logging
import sys
from abc import ABCMeta, abstractmethod
from unittest import mock

from pydantic import BaseModel

from src.adapters.cache.cache_interfaces import CacheInterface
from src.domain.exceptions.exceptions import ClientNotFoundException
from src.domain.models.repository.output import ClientModel
from src.domain.services.client_service import ClientService

class UseCaseInterface(metaclass=ABCMeta):

    def __init__(
            self, cache: CacheInterface, 
            logger: logging.Logger, 
            client_service: ClientService
) -> None:
        self.cache = cache
        self.logger = logger
        self.client_service = client_service

    @classmethod
    async def init(
        cls, 
        cache: CacheInterface, 
        logger: logging.Logger, 
        client_service: ClientService
):
        if "pytest" in sys.argv[0]:
            return cls(cache, logger, mock.Mock(), client_service)

        return cls(cache, logger, client_service)


    async def _get_client_by_hash(self, x_client_hash: str) -> ClientModel:
        client = await self.client_service.get_client_by_hash(x_client_hash)
        if not client:
            raise ClientNotFoundException({"x_client_hash": x_client_hash})
        return client

    @abstractmethod
    def process(self, input_data: BaseModel):
        raise NotImplementedError
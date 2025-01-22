import logging
import sys
from abc import ABCMeta, abstractmethod

from pydantic import BaseModel

from domain.models.repository.output import ClientModel

class UseCaseInterface(metaclass=ABCMeta):

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(
            f"{self.__module__}.{self.__class__.__name__}"
        )
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    async def _get_client_by_hash(self, x_client_hash: str) -> ClientModel:
        client = await ClientModel.get(x_client_hash=x_client_hash)
        if not client:
            raise Exception("Client not found")
        return client

    @abstractmethod
    def process(self, input_data: BaseModel):
        raise NotImplementedError
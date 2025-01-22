import logging
from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel

from adapters.cache.cache_interfaces import CacheInterface
from domain.models.enums import StepNames
from domain.models.repository.output import ClientModel, ClientValidationErrors
from domain.models.usecases.output import StepModelOutput


class StepInterface(metaclass=ABCMeta):
    def __init__(
        self,
        logger: logging.Logger,
        client: ClientModel,
        cache: CacheInterface,
    ):
        """
        Interface base para Steps.

        :param logger: Instância do logger.
        :param settings: Configurações do aplicativo.
        :param client: Dados do cliente sendo processado.
        :param cache: Interface de cache para persistência temporária.
        """
        self.cache = cache
        self.logger = logger
        self.client = client
        self.update_data: dict = {}
        self.validation_errors: list[ClientValidationErrors] = []
        self.update_next_step: bool = True

    @property
    @abstractmethod
    def name(self) -> StepNames:
        """
        Nome do Step correspondente.
        """
        pass

    @property
    @abstractmethod
    def info(self) -> dict:
        """
        Informações adicionais sobre o Step.
        """
        raise NotImplementedError

    @abstractmethod
    async def run_step(self, step_data: Optional[BaseModel] = None) -> StepModelOutput:
        """
        Executa a lógica principal do Step.

        :param step_data: Dados de entrada para o Step.
        :return: Resultado da execução do Step.
        """
        raise NotImplementedError

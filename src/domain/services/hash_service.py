import hashlib
import logging
from datetime import datetime
from typing import Optional


from src.domain.services.client_service import ClientService
from src.adapters.cache.cache_interfaces import CacheInterface
from src.domain.exceptions.exceptions import HashNotFoundException
from src.domain.models.api.input import CreateHashInput
from src.domain.models.api.output import HashOutput
from src.domain.models.enums import ClientStatus
from src.domain.models.repository.output import HashModel


class CreateHashService:
    def __init__(
            self,
            cache: CacheInterface,
            logger: logging.Logger,
            step_data: CreateHashInput,
            client_service: ClientService,
    ):
        self.cache = cache
        self.logger = logger
        self.step_data = step_data
        self.client_service = client_service
        self.client_repository = client_service.client_repository
    
    def _create_hash_string(self):
        string = bytes(f"{self.step_data.name}{self.step_data.device_id}", "utf-8")
        sha512 = hashlib.sha512()
        sha512.update(string)
        hash_string = sha512.hexdigest()

        return hash_string
    
    async def _get_existing_hash(self) -> Optional[HashModel]:
        try:
            return await self.client_repository.get_hash(name=self.step_data.name)
        except HashNotFoundException:
            return None
    
    async def _save_hash(self, hash_string: str):
        hash_data = await self._get_existing_hash()
        name = self.step_data.name

        if not hash_data or hash_data.key != hash_string:
            self.logger.info(f"First time hash or hash changed for {name}")
            try:
                client = await self.client_repository.get_client_by_name(name)
                if client.status != ClientStatus.COMPLETED:
                    try:
                        client.status = ClientStatus.ABANDONED
                        client.updated_at.append({"date": datetime.now(), "user": "onboarding"})
                    except Exception as e:
                        self.logger.error(f"Error updating client: {e}")
            
            except Exception as exc:
                client = exc.client if isinstance(exc, HashNotFoundException) else None
                await self.client_repository.delete_client(client)
            if hash_data:
                await self.cache.delete_item(f"client:{hash_data.key}")
                await self.client_repository.delete_hash(name)

            await self.client_repository.create_hash({"name": name, "key": hash_string})
    
        await self.cache.set_item(f"client:{hash_string}", self.step_data.name, 1800)
    
    async def run(self) -> HashOutput:
        try:
            hash_string = self._create_hash_string()
            await self._save_hash(hash_string)
            return HashOutput(key=hash_string)
        except Exception as e:
            self.logger.critical("Unknown error on create hash")
            raise e


from domain.interfaces.usecases import UseCaseInterface

from domain.models.repository.output import ClientModel

class GetClientUseCase(UseCaseInterface):
    async def process(self, hash_code: str) -> ClientModel:
        return await self._get_client_by_hash(hash_code)

from src.domain.interfaces.usecases import UseCaseInterface
from src.domain.models.api.input import CreateHashInput
from src.domain.models.api.output import HashOutput
from src.domain.services.hash_service import CreateHashService

class CreateHashUseCase(UseCaseInterface):
    async def process(self, body: CreateHashInput) -> HashOutput:
        hash_service = CreateHashService(
                self.cache,
                self.logger,
                body,
                self.client_service,
        )
        output = await hash_service.run()
        return output
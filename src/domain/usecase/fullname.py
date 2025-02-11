from src.domain.interfaces.usecases import UseCaseInterface
from src.domain.models.api.input import FullnameInput
from src.domain.models.enums import StepNames
from src.domain.models.repository.output import ClientModel
from src.domain.models.usecases.output import StepModelOutput
from src.domain.models.services.input import StepActivityInput


class FullnameUseCase(UseCaseInterface):
    async def _run_process(self, body: FullnameInput, client: ClientModel) -> StepModelOutput:
        step_input = StepActivityInput(
            step_name=StepNames.FULLNAME, step_data=body, client=client
        )
        return await (step_input)
    
    async def process(self, body: FullnameInput, x_client_hash: str) -> StepModelOutput:
        client = await self._get_client_by_hash(x_client_hash)
        return await self._run_process(body, client=client)

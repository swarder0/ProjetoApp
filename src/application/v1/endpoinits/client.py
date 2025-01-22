from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException

router = APIRouter(
    tags=["cadastro"],
    responses={
        HTTPStatus.UNAUTHORIZED.value: {"description": "Não autorizado"},
        HTTPStatus.FORBIDDEN.value: {"description": "Acesso negado"},
        HTTPStatus.NOT_FOUND.value: {"description": "Não encontrado"},
    }
)

@router.get(
    "/cadastro",
    summary="Cadastro",
    description="Visualizar um cadastro do cliente pelo login",
    )
async def get_cadastro():
        
        return {"message": "Cadastro de usuários"}

@router.post(
    "/cadastro",
    summary="Criar cadastro",
    description="Cria um novo cadastro",
    )
async def create_client_cadaster():

        return {"message": "Cadastro de usuários"}

@router.delete(
    "/cadastro",
    summary="Deletar cadastro",
    description="Deleta um cadastro",
    )

async def delete_client_cadaster():

        return {"message": "Cadastro de usuários"}

@router.post(
    "/cadastro/fullname",
    summary="Atualizar nome",
    description="Atualiza um cadastro com o nome completo do cliente",
    )
async def fullname():

        return {"message": "Inserindo nome do client"}

@router.post(
        "/cadastro/birth_date",
        summary="Atualizar data de nascimento",
        description="Atualiza um cadastro com a data de nascimento do cliente",
)
async def birth_date():

        return {"message": "Inserindo data de nascimento do client"}

@router.post(
        "/cadastro/phone",
        summary="Atualizar telefone",
        description="Atualiza um cadastro com o telefone do cliente",
)
async def phone():

        return {"message": "Inserindo telefone do client"}

@router.post(
        "/cadastro/address",
        summary="Atualizar endereço",
        description="Atualiza um cadastro com o endereço do cliente",
)
async def address():

        return {"message": "Inserindo endereço do client"}

@router.post(
        "/cadastro/email",
        summary="Atualizar email",
        description="Atualiza um cadastro com o email do cliente",
)
async def email():

        return {"message": "Inserindo email do client"}(
)

@router.post(
        "/cadastro/password",
        summary="Atualizar senha",
        description="Atualiza um cadastro com a senha do cliente",
)
async def password():

        return {"message": "Inserindo senha do client"}

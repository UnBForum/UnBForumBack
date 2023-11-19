from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.main import app
from src.schemas.user import UserRetrieveSchema

client = TestClient(app)
scenarios('../../features/user/test_current_user.feature')


@when(
    'O endpoint "GET /users/me" é chamado com o token de autenticação',
    target_fixture='response'
)
def get_current_user_request(user, get_token):
    headers = {'Authorization': f'Bearer {get_token(user.email)}'}
    response = client.get('/users/me', headers=headers)
    return response

@when(
    'O endpoint "GET /users/me" é chamado com o token de autenticação incorreto',
    target_fixture='response'
)
def get_incorrect_user_request():
    headers = {'Authorization': f'Bearer token_invalido'}
    response = client.get('/users/me', headers=headers)
    return response

@when(
    'O endpoint "PATCH /users/me" é chamado com o token de autenticação',
    target_fixture='response'
)
def update_current_user_request(user, get_token):
    data = {'name': 'Novo Nome de Usuário'}
    headers = {'Authorization': f'Bearer {get_token(user.email)}'}
    response = client.patch('/users/me', json=data, headers=headers)
    return response

@when(
    'O endpoint "DELETE /users/me" é chamado com o token de autenticação',
    target_fixture='response'
)
def delete_current_user_request(user, get_token):
    headers = {'Authorization': f'Bearer {get_token(user.email)}'}
    response = client.delete('/users/me', headers=headers)
    return response

@then('A resposta contém os dados do usuário')
def check_response_body(response):
    assert response.json().keys() == UserRetrieveSchema.model_fields.keys()
    user = UserRetrieveSchema(**response.json())
    assert user.id is not None

@then('A resposta contém os dados atualizados do usuário')
def check_updated_user(response):
    assert response.json().keys() == UserRetrieveSchema.model_fields.keys()
    user = UserRetrieveSchema(**response.json())
    assert user.name == 'Novo Nome de Usuário'

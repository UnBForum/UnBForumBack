from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.main import app
from src.schemas.auth import TokenData


client = TestClient(app)
scenarios('../../features/auth/login.feature')


@given(parsers.parse('O usuário possui uma conta cadastrada com o email "{email}" e senha "{password}"'))
def given_a_registered_user(create_user, email, password):
    create_user(email, password)


@when(
    parsers.parse('O endpoint "POST /auth/login" é chamado com o email "{email}" e senha "{password}"'),
    target_fixture='response',
)
def login_request(email, password):
    body = {'username': email, 'password': password}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post('/auth/login', data=body, headers=headers)
    return response


@then('O corpo da resposta contém o token de autenticação')
def check_response_body(response):
    token_data = TokenData(**response.json())
    assert token_data.access_token is not None
    assert token_data.token_type == 'bearer'

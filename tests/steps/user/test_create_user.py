from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.main import app
from src.schemas.user import UserRetrieveSchema

client = TestClient(app)
scenarios('../../features/user/create_user.feature')


@given(parsers.parse('Já existe um usuário cadastrado com o email {email}'))
def given_a_user_already_exists(create_user, email):
    create_user(email)

@when(
    parsers.cfparse(
        'O endpoint "POST /users" é chamado com os dados {email:String}, {password:String}, {tags:String*}',
        extra_types={'String': str}),
    target_fixture='response'
)
def create_user_request(email, password, tags):
    user = {
        'name': 'Usuário de Testes',
        'email': email,
        'password': password,
        'tags': tags,
    }
    response = client.post('/users', json=user)
    return response


@then(parsers.parse('A resposta contém o usuário criado com o {email}'))
def check_response_body(response, email):
    assert response.json().keys() == UserRetrieveSchema.model_fields.keys()
    user = UserRetrieveSchema(**response.json())
    assert user.id is not None
    assert user.email == email

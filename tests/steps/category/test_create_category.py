from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.main import app
from src.schemas.category import CategoryRetrieveSchema

client = TestClient(app)
scenarios('../../features/category/test_create_category.feature')


@given(parsers.parse('Uma categoria com o nome {name} já existe'))
def given_a_category_already_exists(create_category, name):
    create_category(name)

@when(
    parsers.parse('O endpoint "POST /categories" é chamado com o nome {name} e cor {color}'),
    target_fixture='response'
)
def create_category_request(user, get_token, name, color):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    category = {'name': name, 'color': color}
    response = client.post('/categories', json=category, headers=headers)
    return response


@then(parsers.parse('A resposta contém a categoria criada com {name} e {color}'))
def check_response_body(response, name, color):
    assert response.json().keys() == CategoryRetrieveSchema.model_fields.keys()
    category = CategoryRetrieveSchema(**response.json())
    assert category.id is not None
    assert category.name == name
    assert category.color == color

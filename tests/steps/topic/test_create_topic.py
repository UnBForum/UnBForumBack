from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.main import app
from src.schemas.topic import TopicRetrieveSchema


client = TestClient(app)
scenarios('../../features/topic/test_create_topic.feature')
EXTRA_TYPES = {'Integer': int}


@given(parsers.cfparse('As categorias com ids {categories:Integer*} já existem', extra_types=EXTRA_TYPES))
def given_a_category_already_exists(create_category, categories):
    for category_id in categories:
        create_category(id_=category_id, name=f'Categoria_{category_id}')


@given(parsers.cfparse('Os arquivos com ids {files:Integer*} já existem', extra_types=EXTRA_TYPES))
def given_a_file_already_exists(create_file, files):
    for file_id in files:
        create_file(id_=file_id)


@when(
    parsers.cfparse(
        'O endpoint "POST /topics" é chamado com os dados {title}, {content}, {categories:Integer*} e {files:Integer*}.',
        extra_types=EXTRA_TYPES),
    target_fixture='response'
)
def create_topic_request(user, get_token, title, content, categories, files):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    print(categories)
    topic = {'title': title, 'content': content, 'categories': categories, 'files': files}
    response = client.post('/topics/', json=topic, headers=headers)
    return response


@then(parsers.parse('A resposta contém o tópico criado'))
def check_response_body(response):
    assert response.json().keys() == TopicRetrieveSchema.model_fields.keys()

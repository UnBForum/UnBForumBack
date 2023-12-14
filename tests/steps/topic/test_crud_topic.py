from typing import List

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User, Topic
from src.main import app


client = TestClient(app)
scenarios(
    '../../features/topic/create_topic.feature',
    '../../features/topic/edit_topic.feature',
    '../../features/topic/delete_topic.feature'
)
EXTRA_TYPES = {'d': int}


@given(parsers.parse('Um tópico com id {topic_id:d} criado pelo usuário autenticado'))
def given_a_topic_already_exists(topic_id: int, create_topic, user: User):
    create_topic(id_=topic_id, user_id=user.id)


@given(parsers.parse('Um tópico com id {topic_id:d} criado por outro usuário'))
def given_a_topic_created_by_other_user(topic_id: int, create_topic, create_user, user: User):
    other_user = create_user(email='other_user@unb.br')
    create_topic(id_=topic_id, user_id=other_user.id)


@given(parsers.cfparse('As categorias com ids {categories:d*} já existem', extra_types=EXTRA_TYPES))
def given_a_category_already_exists(create_category, categories):
    for category_id in categories:
        create_category(id_=category_id, name=f'Categoria_{category_id}')


@given(parsers.cfparse('Os arquivos com ids {files:d*} já existem', extra_types=EXTRA_TYPES))
def given_a_file_already_exists(create_file, files):
    for file_id in files:
        create_file(id_=file_id)


@when(
    parsers.cfparse(
        'O endpoint "POST /topics/" é chamado com os dados {title}, {content}, {categories:d*} e {files:d*}.',
        extra_types=EXTRA_TYPES),
    target_fixture='response'
)
def create_topic_request(title: str, content: str, categories: List[str], files: List[str], user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    topic = {'title': title, 'content': content, 'categories': categories, 'files': files}
    response = client.post('/topics/', json=topic, headers=headers)
    return response


@when(
    parsers.cfparse(
        'O endpoint "PUT /topics/{topic_id:d}/" é chamado com os dados {title}, {content}, {categories:d*} e {files:d*}.',
        extra_types=EXTRA_TYPES),
    target_fixture='response'
)
def update_topic_request(
        topic_id: int, title: str, content: str, categories: List[str], files: List[str], user: User, get_token
):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    topic = {'title': title, 'content': content, 'categories': categories, 'files': files}
    response = client.put(f'/topics/{topic_id}/', json=topic, headers=headers)
    return response


@when(
    parsers.cfparse(
        'O endpoint "DELETE /topics/{topic_id:d}/" é chamado',
        extra_types=EXTRA_TYPES),
    target_fixture='response'
)
def delete_topic_request(topic_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.delete(f'/topics/{topic_id}/', headers=headers)
    return response


@then(parsers.cfparse(
    'O tópico é criado com os dados {title}, {content}, {categories:d*} e {files:d*}.',
    extra_types=EXTRA_TYPES)
)
@then(parsers.cfparse(
    'O tópico é atualizado com os dados {title}, {content}, {categories:d*} e {files:d*}.',
    extra_types=EXTRA_TYPES)
)
def check_updated_topic(title: str, content: str, categories: List[str], files: List[str], response):
    topic = response.json()
    assert topic['title'] == title
    assert topic['content'] == content
    assert [category['id'] for category in topic['categories']] == categories
    assert [file['id'] for file in topic['files']] == files


@then(parsers.parse('O tópico com id {topic_id:d} é apagado'))
def check_deleted_topic(topic_id: int, db_session: Session):
    assert Topic.get_one(db_session, id=topic_id) is None

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User, Comment
from src.main import app


client = TestClient(app)
scenarios(
    '../../features/comment/create_comment.feature',
    '../../features/comment/delete_comment.feature',
    '../../features/comment/edit_comment.feature'
)


@given(parsers.parse('Um comentário com id {comment_id:d} adicionado ao tópico {topic_id:d} pelo usuário autenticado'))
def given_a_comment_already_exists(topic_id: int, comment_id:int, create_comment, user: User):
    create_comment(id_=comment_id, topic_id=topic_id, user_id=user.id)


@given(parsers.parse('Um comentário com id {comment_id:d} adicionado ao tópico {topic_id:d} por outro usuário'))
def given_a_comment_created_by_other_user(topic_id: int, comment_id:int, create_comment, create_user):
    other_user = create_user(email='other_user@unb.br')
    create_comment(id_=comment_id, topic_id=topic_id, user_id=other_user.id)


@when(
    parsers.parse('O endpoint "POST /topics/{topic_id:d}/comments/" é chamado com o conteúdo {content}'),
    target_fixture='response'
)
def create_comment_request(topic_id: int, content: str, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    comment_body = {'content': content}
    response = client.post(f'/topics/{topic_id}/comments/', json=comment_body, headers=headers)
    return response


@when(
    parsers.parse('O endpoint "PUT /topics/{topic_id:d}/comments/{comment_id:d}/" é chamado com o conteúdo {content}'),
    target_fixture='response'
)
def update_comment_request(topic_id: int, comment_id: int, content: str, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    comment_body = {'content': content}
    response = client.put(f'/topics/{topic_id}/comments/{comment_id}', json=comment_body, headers=headers)
    return response


@when(
    parsers.parse('O endpoint "DELETE /topics/{topic_id:d}/comments/{comment_id:d}/" é chamado'),
    target_fixture='response'
)
def delete_comment_request(topic_id: int, comment_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.delete(f'/topics/{topic_id}/comments/{comment_id}/', headers=headers)
    return response


@then(parsers.parse('O comentário é criado com o conteúdo {content}'))
@then(parsers.parse('O comentário é atualizado com o conteúdo {content}'))
def check_response_content(content: str, response):
    assert response.json()["content"] == content


@then(parsers.parse('O comentário com id {comment_id:d} é apagado'))
def check_deleted_comment(comment_id: int, db_session: Session):
    assert Comment.get_one(db_session, id=comment_id) is None

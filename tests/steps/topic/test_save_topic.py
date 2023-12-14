from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User, USER_saves_TOPIC
from src.main import app


client = TestClient(app)
scenarios('../../features/topic/save_topic.feature')


@given(parsers.parse('O tópico com id {topic_id:d} está salvo pelo usuário'))
@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/save/" é chamado'), target_fixture='response')
def save_topic_request(topic_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/save/', headers=headers)
    return response


@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/unsave/" é chamado'), target_fixture='response')
def unsave_topic_request(topic_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/unsave/', headers=headers)
    return response


@then(parsers.parse('O tópico com id {topic_id:d} é salvo pelo usuário'))
def check_topic_is_saved_by_user(topic_id: int, user: User, db_session: Session):
    assert db_session.query(USER_saves_TOPIC).filter_by(user_id=user.id, topic_id=topic_id).count() == 1


@then(parsers.parse('O tópico com id {topic_id:d} é removido dos tópicos salvos pelo usuário'))
def check_response(topic_id: int, user: User, db_session):
    assert db_session.query(USER_saves_TOPIC).filter_by(user_id=user.id, topic_id=topic_id).count() == 0

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User, Topic
from src.main import app


client = TestClient(app)
scenarios('../../features/topic/fix_topic.feature')


@given(parsers.parse('Um tópico com id {topic_id:d}'))
def given_a_topic_already_exist(topic_id: int, user: User, create_topic):
    create_topic(id_=topic_id, user_id=user.id)


@given(parsers.parse('O tópico com id {topic_id:d} está fixado'))
@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/fix/" é chamado'), target_fixture='response')
def save_topic_request(topic_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/fix/', headers=headers)
    return response


@then(parsers.parse('O tópico com id {topic_id:d} é fixado'))
def check_topic_is_fixed(topic_id: int, db_session: Session):
    assert Topic.get_one(db_session, id=topic_id).is_fixed


@then(parsers.parse('O tópico com id {topic_id:d} é desafixado'))
def check_topic_is_not_fixed(topic_id: int, db_session: Session):
    assert not Topic.get_one(db_session, id=topic_id).is_fixed

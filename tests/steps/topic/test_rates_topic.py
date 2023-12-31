from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User, Topic
from src.main import app


client = TestClient(app)
scenarios('../../features/topic/rates_topic.feature')


@given(parsers.parse('O tópico com id {topic_id:d} já foi avaliado positivamente pelo usuário'))
@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/upvote/" é chamado'), target_fixture='response')
def upvote_topic_request(topic_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/upvote/', headers=headers)
    return response


@given(parsers.parse('O tópico com id {topic_id:d} já foi avaliado negativamente pelo usuário'))
@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/downvote/" é chamado'), target_fixture='response')
def downvote_topic_request(topic_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/downvote/', headers=headers)
    return response


@then(parsers.parse('O tópico com id {topic_id:d} possui rating {rating:d}'))
def check_topic_rating(topic_id: int, rating: int, db_session: Session):
    assert Topic.get_one(db_session, id=topic_id).rating == rating

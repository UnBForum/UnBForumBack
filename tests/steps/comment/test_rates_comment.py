from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User, Comment
from src.main import app


client = TestClient(app)
scenarios('../../features/comment/rates_comment.feature')


@given(parsers.parse('Um comentário com id {comment_id:d} adicionado ao tópico {topic_id:d}'))
def given_a_comment_already_exist(comment_id: int, topic_id: int, user: User, create_comment):
    create_comment(id_=comment_id, topic_id=topic_id, user_id=user.id)


@given(parsers.parse('O comentário com id {comment_id:d} do tópico {topic_id:d} já foi avaliado positivamente pelo usuário'))
@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/comments/{comment_id:d}/upvote/" é chamado'), target_fixture='response')
def upvote_comment_request(topic_id: int, comment_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/comments/{comment_id}/upvote/', headers=headers)
    return response


@given(parsers.parse('O comentário com id {comment_id:d} do tópico {topic_id:d} já foi avaliado negativamente pelo usuário'))
@when(parsers.parse('O endpoint "POST /topics/{topic_id:d}/comments/{comment_id:d}/downvote/" é chamado'), target_fixture='response')
def downvote_comment_request(topic_id: int, comment_id: int, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    response = client.post(f'/topics/{topic_id}/comments/{comment_id}/downvote/', headers=headers)
    return response


@then(parsers.parse('O comentário com id {comment_id:d} possui rating {rating:d}'))
def check_topic_rating(comment_id: int, rating: int, db_session: Session):
    assert Comment.get_one(db_session, id=comment_id).rating == rating

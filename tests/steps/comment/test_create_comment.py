from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.db.models import User
from src.main import app


client = TestClient(app)
scenarios('../../features/comment/create_comment.feature')


@when(
    parsers.parse('O endpoint "POST /topics/{topic_id:d}/comments/" é chamado com o conteúdo {content}'),
    target_fixture='response'
)
def create_comment_request(topic_id: int, content: str, user: User, get_token):
    headers = {'Authorization': f'Bearer {get_token(user)}'}
    comment_body = {'content': content}
    response = client.post(f'/topics/{topic_id}/comments/', json=comment_body, headers=headers)
    return response


@then(parsers.parse('O comentário criado possui o conteúdo {content}'))
def check_response_body(content: str, response):
    assert response.json()["content"] == content

import pytest
from pytest_bdd import given, then, parsers
from passlib.context import CryptContext

from src.db.connection import LocalSession
from src.db.models import User, Tag, Category, File, Topic
from src.utils.jwt import create_access_token

crypt_context = CryptContext(schemes=['sha256_crypt'])

def _clean_database(db_session):
    Tag.delete_all(db_session)
    User.delete_all(db_session)
    Category.delete_all(db_session)
    Topic.delete_all(db_session)

# Hooks

def pytest_bdd_before_scenario(request, feature, scenario):
    _clean_database(request.getfixturevalue('db_session'))

def pytest_bdd_after_scenario(request, feature, scenario):
    _clean_database(request.getfixturevalue('db_session'))

# Fixtures

@pytest.fixture()
def db_session():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def get_token(request):
    def _token(user):
        return create_access_token(user)
    return _token

@pytest.fixture()
def create_user(db_session, request):
    def _create_user(email='johndoe@unb.br', password='teste_senha', role='member'):
        user = User(name='Usuário de Testes', email=email, role=role, password=crypt_context.hash(password))
        user.save(db_session)

        return user

    yield _create_user

    request.addfinalizer(lambda: User.delete_all(db_session))


@pytest.fixture()
def create_tag(db_session, request):
    def _create_tag(name='Tag'):
        tag = Tag(name=name)
        tag.save(db_session)

        return tag

    yield _create_tag

    request.addfinalizer(lambda: Tag.delete_all(db_session))


@pytest.fixture()
def create_category(db_session, request):
    def _create_category(id_=1, name='TCC', color='#10B981'):
        category = Category(id=id_, name=name, color=color)
        category.save(db_session)

        return category

    yield _create_category

    request.addfinalizer(lambda: Category.delete_all(db_session))


@pytest.fixture()
def create_file(db_session, request):
    def _create_file(id_=1, name='Arquivo', content_type='image/jpg', upload_path='/path/file.jpg'):
        file = File(id=id_, name=name, content_type=content_type, upload_path=upload_path)
        file.save(db_session)

        return file

    yield _create_file

    request.addfinalizer(lambda: File.delete_all(db_session))


@pytest.fixture()
def create_topic(db_session, request):
    def _create_topic(id_=1, title='Título', content='Descrição', user_id=1, is_fixed=False):
        topic = Topic(id=id_, title=title, content=content, user_id=user_id, is_fixed=is_fixed)
        topic.save(db_session)

        return topic

    yield _create_topic

    request.addfinalizer(lambda: Topic.delete_all(db_session))

# Common Steps

@given('Um usuário visitante')
def given_a_guest_user():
    pass

@given('Um usuário autenticado (membro)', target_fixture='user')
def given_a_authenticated_user(create_user):
    return create_user(role='member')

@given('Um usuário autenticado (moderador)', target_fixture='user')
def given_a_authenticated_moderator(create_user):
    return create_user(role='moderator')

@given('Um usuário autenticado (administrador)', target_fixture='user')
def given_a_authenticated_admin(create_user):
    return create_user(role='administrator')

@given(parsers.parse('Um tópico com id {topic_id:d}'))
def given_a_topic_already_exist(topic_id: int, user: User, create_topic):
    create_topic(id_=topic_id, user_id=user.id)

@then(parsers.parse('O status da resposta é "{code:d}"'))
def check_status_code(response, code):
    assert response.status_code == code

@then(parsers.parse('A resposta contém a mensagem de erro "{error_msg}"'))
def check_error_message(response, error_msg):
    assert response.json()['detail'] == error_msg

import pytest
from pytest_bdd import given, then, parsers
from passlib.context import CryptContext

from src.db.connection import LocalSession
from src.db.models import User, Tag
from src.utils.jwt import create_access_token

crypt_context = CryptContext(schemes=['sha256_crypt'])

def _create_default_tags(db_session):
    Tag(name='Engenharias').save(db_session)
    Tag(name='Engenharia Aeroespacial').save(db_session)
    Tag(name='Engenharia Automotiva').save(db_session)
    Tag(name='Engenharia de Energia').save(db_session)
    Tag(name='Engenharia de Software').save(db_session)
    Tag(name='Engenharia Eletrônica').save(db_session)

    Tag(name='Estudante').save(db_session)
    Tag(name='Professor').save(db_session)
    Tag(name='Técnico').save(db_session)

def _clean_database(db_session):
    Tag.delete_all(db_session)
    User.delete_all(db_session)

# Hooks

def pytest_bdd_before_scenario(request, feature, scenario):
    _clean_database(request.getfixturevalue('db_session'))
    _create_default_tags(request.getfixturevalue('db_session'))

def pytest_bdd_after_scenario(request, feature, scenario):
    _clean_database(request.getfixturevalue('db_session'))

# Fixtures

@pytest.fixture()
def db_session():
    try:
        session = LocalSession()
        yield session
    finally:
        session.close()

@pytest.fixture()
def get_token(request):
    def _token(email='johndoe@unb.br'):
        return create_access_token(email)
    return _token

@pytest.fixture()
def create_user(db_session, request):
    def _create_user(email='johndoe@unb.br', password='teste_senha', role='member'):
        user = User(
            name='Usuário de Testes',
            email=email,
            role=role,
            password=crypt_context.hash(password)
        )
        user.save(db_session)

        return user

    yield _create_user

    request.addfinalizer(lambda: User.delete_all(db_session))

# Common Steps

@given('Um usuário visitante')
def given_a_guest_user():
    pass

@given('Um usuário autenticado (membro)', target_fixture='user')
def given_a_authenticated_user(create_user):
    return create_user(role='member')

@given('Um usuário autenticado (moderator)', target_fixture='user')
def given_a_authenticated_admin(create_user):
    return create_user(role='moderator')

@given('Um usuário autenticado (administrator)', target_fixture='user')
def given_a_authenticated_admin(create_user):
    return create_user(role='administrator')

@then(parsers.parse('O status da resposta é "{code:d}"'))
def check_status_code(response, code):
    assert response.status_code == code

@then(parsers.parse('A resposta contém a mensagem de erro "{error_msg}"'))
def check_error_message(response, error_msg):
    assert response.json()['detail'] == error_msg

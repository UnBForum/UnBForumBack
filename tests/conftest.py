import pytest
from pytest_bdd import then, parsers
from passlib.context import CryptContext

from src.db.connection import LocalSession
from src.db.models import User

crypt_context = CryptContext(schemes=['sha256_crypt'])


@pytest.fixture
def db_session():
    try:
        session = LocalSession()
        yield session
    finally:
        session.close()


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

@then(parsers.parse('O status da resposta é "{code:d}"'))
def check_status_code(response, code):
    assert response.status_code == code

from src.db.connection import LocalSession


def get_db_session():
    try:
        session = LocalSession()
        yield session
    finally:
        session.close()

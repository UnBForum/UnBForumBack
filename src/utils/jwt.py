from jose import jwt
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


def create_access_token(user_email: str):
    data = {"sub": user_email}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

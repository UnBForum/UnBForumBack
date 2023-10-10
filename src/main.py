from fastapi import FastAPI

from src.routes.user import user_router

app = FastAPI()


@app.get('/')
def home():
    return {"hello": "world"}


app.include_router(user_router)

from fastapi import FastAPI

from src.routers import auth_router, user_router, topic_router, category_router, comment_router

app = FastAPI()


@app.get('/')
def home():
    return {"hello": "world"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(topic_router)
app.include_router(category_router)
app.include_router(comment_router)
from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment
from fastapi.staticfiles import StaticFiles
from auth import authentication

app = FastAPI()


@app.get("/")
def root():
    return "Hello World"


app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)
app.mount("/images", StaticFiles(directory="images"), name="image")


models.Base.metadata.create_all(engine)

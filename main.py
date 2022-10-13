from fastapi import FastAPI
from db import models
from db.database import engine
from routers import user, post, comment
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddlewares

app = FastAPI()


@app.get("/")
def root():
    return "Hello World"


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddlewares,
    all_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)

app.mount("/images", StaticFiles(directory="images"), name="image")


models.Base.metadata.create_all(engine)

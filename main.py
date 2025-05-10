from random import randrange
import time
from fastapi import APIRouter, FastAPI, Response ,status,HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models, schemas , utils
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .database import get_db
from .routers import posts,users,auth

router = APIRouter()

models.Base.metadata.create_all(bind = engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostSchema):
    id: int

    class Config:
        orm_mode = True



# ---------- CREATE ----------
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostSchema, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# ---------- READ ALL ----------
@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

# ---------- READ ONE ----------
@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# ---------- UPDATE ----------
@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostSchema, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post

# ---------- DELETE ----------
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}


@app.post("/users" , status_code = status.HTTP_201_CREATED)
def createuser(user : schemas.UserCreate , db : Session = Depends(get_db), response_model = schemas.UserOut):
    hashed = utils.hash(user.password)
    user.password = hashed
    new_post = models.user(**user.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
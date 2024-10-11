from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List

from models import Hero
from database import create_db_and_tables, engine

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session



@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Read all heroes
@app.get("/heroes/", response_model=List[Hero])
def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes


# Read a hero by ID
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.put("/heroes/{heroes_id}", response_model=Hero)
def update_task(heroes_id: int, updated_task: Hero, session: Session = Depends(get_session)):
    hero = session.get(Hero, heroes_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero.name = updated_task.name
    hero.secret_name= updated_task.secret_name
    hero.age = updated_task.age
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.delete("/heroes/{heroes_id}", response_model=Hero)
def update_task(heroes_id: int, updated_task: Hero, session: Session = Depends(get_session)):
    hero = session.get(Hero, heroes_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"detail": "Task deleted"}



from fastapi import FastAPI, Depends, HTTPException
from auth.authentication import oauth2_scheme, get_current_user, create_access_token
from models import User
from data.user import users_db





@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}! This is a protected resource."}



from fastapi import FastAPI, Depends,HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from location.config.db import create_tables, engine
from location.models import *



@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
   

app:FastAPI = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.post("/signup/")
def create_Signup(hero: Signups):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return {
        "success":True
        }
 
 
@app.post("/login/")
def create_Login(hero: Logins):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return {
        "success":True,
    }
        

@app.get("/itemlist/")
def get_data():
    with Session(engine) as session:
        heroes = session.exec(select(Additems)).all()
        return heroes
    
@app.post("/fooditem/")
def create_Login(hero: Additems):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return {
        "success":True,
    }   


@app.delete("/delete/")
def delete_hero(id: int):
    with Session(engine) as session:
        statement = select(Additems).where(Additems.id == id)
        result = session.exec(statement).one_or_none()
        if result:
            session.delete(result)
            session.commit()
            return {"message": "Item deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
        



@app.get("/editlist/")
def get_dataforEditItem(id: int):
    with Session(engine) as session:
        # Construct the query with the filtering condition
        query = select(Additems).where(Additems.id == id)
        
        # Execute the query and fetch the result
        item = session.exec(query).first()  # Get the single result
        
        return item
    
@app.put("/updatelist/")
def update_heroes(id:int , update:Additems):
    with Session(engine) as session:
        # Fetch the item by its ID
        statement = select(Additems).where(Additems.id == id)
        results = session.exec(statement)
        hero = results.one()

        # Update the attributes of the item
        hero.name = update.name
        hero.description = update.description
        hero.price = update.price
        hero.image = update.image

        session.add(hero)
        session.commit()
        session.refresh(hero)
        return "Item updated successfully"


    


def start():
    create_tables()
    uvicorn.run("location.main:app", host="127.0.0.1", port=8080, reload=True)


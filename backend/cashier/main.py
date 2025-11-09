
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel

SQLITE_URL = 'sqlite://'

connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

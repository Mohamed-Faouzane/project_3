from fastapi import FastAPI
from database import engine, Base
from routers import notes, users

# Create all database variables
Base.metadata.create_all(bind = engine) # reads all classes that inherited from "Base" and creates their tables in PostgreSQL

app = FastAPI()

# Register routers
app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Notes API is running"}
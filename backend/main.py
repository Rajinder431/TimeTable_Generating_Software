from fastapi import FastAPI
from app.utils.db import SessionLocal
from app.utils.db import Base, engine
from app.models.classroom import Classroom

app = FastAPI()

@app.post("/create-classroom/")
def create_classroom():
    db = SessionLocal()  # Get a session from the session maker
    new_class = Classroom(name="FY", semester=1)  # Create a new Classroom instance
    db.add(new_class)  # Add the new classroom to the session
    db.commit()  # Commit the transaction to save to the database
    db.refresh(new_class)  # Refresh the instance with data from the database (like auto-generated fields)
    db.close()  # Close the database session
    return new_class  # Return the new classroom instance

# Create tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Timetable Generator backend running 🚀"}

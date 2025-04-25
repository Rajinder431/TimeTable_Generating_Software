# backend/main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from .app.utils.db import SessionLocal, Base, engine
from .app.models.classroom import Classroom
from . import timetable_solver  # Import your timetable function from backend

app = FastAPI()

# --- Root Route ---
@app.get("/")
def root():
    return {"message": "Timetable Generator backend running 🚀"}

# --- Timetable Generation Endpoint ---
@app.post("/generate-timetable/")
def generate():
    result = timetable_solver.generate_timetable()
    return {"timetable": result}  # ✅ This returns the actual generated timetable

# --- Classroom Creation Endpoint ---
@app.post("/create-classroom/")
def create_classroom():
    db = SessionLocal()
    new_class = Classroom(name="FY", semester=1)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    db.close()
    return new_class

# --- Create tables on startup ---
Base.metadata.create_all(bind=engine)

# Inside backend/app/models/classroom.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.db import Base

from sqlalchemy.orm import relationship

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    semester = Column(Integer)

    subjects = relationship("Subject", back_populates="classroom")

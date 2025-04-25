from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..utils.db import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    class_id = Column(Integer, ForeignKey("classrooms.id"))
    lab_required = Column(Boolean, default=False)
    weekly_lectures = Column(Integer)

    classroom = relationship("Classroom", back_populates="subjects")

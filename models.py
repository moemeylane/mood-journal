from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    journal_entries = relationship("JournalEntry", back_populates="user")
    mood_patterns = relationship("MoodPattern", back_populates="user")

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    mood = Column(String, nullable=False)
    content = Column(String, nullable=True)
    
    user = relationship("User", back_populates="journal_entries")

class MoodPattern(Base):
    __tablename__ = "mood_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pattern = Column(String, nullable=False)
    
    user = relationship("User", back_populates="mood_patterns")

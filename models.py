from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Store as plaintext for now

    # Relationship to JournalEntry and MoodPattern
    journal_entries = relationship("JournalEntry", back_populates="user")
    mood_patterns = relationship("MoodPattern", back_populates="user")

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, default=date.today, nullable=False)
    mood = Column(String, nullable=False)
    content = Column(String, nullable=True)

    # Relationship back to User
    user = relationship("User", back_populates="journal_entries")

    def __repr__(self):
        return f"<JournalEntry(mood='{self.mood}', date='{self.date}')>"

class MoodPattern(Base):
    __tablename__ = 'mood_patterns'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pattern = Column(String, nullable=False)

    # Relationship back to User
    user = relationship("User", back_populates="mood_patterns")

    def __repr__(self):
        return f"<MoodPattern(user_id='{self.user_id}', pattern='{self.pattern}')>"

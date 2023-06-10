from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    last_login = Column(DateTime)
    tasks = relationship('Task', back_populates="user")
    

class Task(Base):
    __tablename__ = 'tasks'
    
    task_id = Column(Integer, primary_key=True)
    task_name = Column(String)
    priority = Column(Integer, ForeignKey('priorities.priority_id'))
    status = Column(String)
    notes = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationship with DueDate model
    due_dates = relationship("DueDate", back_populates="task")

    # Relationship with User model
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="tasks")

class DueDate(Base):
    __tablename__ = 'due_dates'
    
    due_date_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.task_id'))
    due_date = Column(DateTime)
    
    # Relationship with Task model
    task = relationship("Task", back_populates="due_dates")


class Priority(Base):
    __tablename__ = 'priorities'
    
    priority_id = Column(Integer, primary_key=True)
    priority_name = Column(String)
    priority_value = Column(Integer)
    
    # Relationship with Task model
    tasks = relationship("Task")
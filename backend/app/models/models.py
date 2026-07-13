from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user")
    saved_items = relationship("SavedItem", back_populates="user")

class Analysis(Base):
    __tablename__ = 'analyses'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content_type = Column(String)  # text, image, url, job
    original_text = Column(Text)
    extracted_text = Column(Text, nullable=True)
    risk_level = Column(String)
    confidence_score = Column(Float)
    scam_probability = Column(Float)
    indicators = Column(Text)  # JSON string
    explanation = Column(Text)  # JSON string
    recommendations = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analyses")

class SavedItem(Base):
    __tablename__ = 'saved_items'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    analysis_id = Column(Integer, ForeignKey('analyses.id'))
    item_type = Column(String)  # analysis, article, quiz_result
    title = Column(String)
    notes = Column(Text, nullable=True)
    is_flagged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_items")
    analysis = relationship("Analysis")

class ScamReport(Base):
    __tablename__ = 'scam_reports'
    
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    scam_type = Column(String)
    description = Column(Text)
    url = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    location = Column(String, nullable=True)
    report_date = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class Monument(Base):
    """Monument table - stores basic monument information"""
    __tablename__ = 'monuments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    state = Column(String(100), nullable=False)
    official_description = Column(Text, nullable=False)
    location = Column(String(200))
    year_built = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_stories = relationship('UserStory', back_populates='monument', cascade='all, delete-orphan')
    generated_stories = relationship('GeneratedStory', back_populates='monument', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Monument {self.name} - {self.state}>'
    
    def to_dict(self):
        """Convert monument to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'official_description': self.official_description,
            'location': self.location,
            'year_built': self.year_built
        }


class UserStory(Base):
    """User stories table - community contributions"""
    __tablename__ = 'user_stories'
    
    id = Column(Integer, primary_key=True)
    monument_id = Column(Integer, ForeignKey('monuments.id'), nullable=False)
    user_text = Column(Text)
    user_audio_path = Column(String(300))
    detected_language = Column(String(10))
    translated_english_text = Column(Text)
    is_approved = Column(Integer, default=0)  # 0=pending, 1=approved, 2=rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    monument = relationship('Monument', back_populates='user_stories')
    
    def __repr__(self):
        return f'<UserStory {self.id} - Monument {self.monument_id}>'
    
    def to_dict(self):
        """Convert user story to dictionary"""
        return {
            'id': self.id,
            'monument_id': self.monument_id,
            'user_text': self.user_text,
            'detected_language': self.detected_language,
            'translated_english_text': self.translated_english_text,
            'is_approved': self.is_approved,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class GeneratedStory(Base):
    """Generated stories table - AI-created stories"""
    __tablename__ = 'generated_stories'
    
    id = Column(Integer, primary_key=True)
    monument_id = Column(Integer, ForeignKey('monuments.id'), nullable=False)
    language = Column(String(10), nullable=False)
    story_text = Column(Text, nullable=False)
    audio_path = Column(String(300))
    play_count = Column(Integer, default=0)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    monument = relationship('Monument', back_populates='generated_stories')
    
    def __repr__(self):
        return f'<GeneratedStory {self.id} - {self.language}>'
    
    def to_dict(self):
        """Convert generated story to dictionary"""
        return {
            'id': self.id,
            'monument_id': self.monument_id,
            'language': self.language,
            'story_text': self.story_text,
            'audio_path': self.audio_path,
            'play_count': self.play_count,
            'generated_at': self.generated_at.strftime('%Y-%m-%d %H:%M:%S') if self.generated_at else None
        }

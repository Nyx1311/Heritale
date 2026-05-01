import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Flask Configuration
class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Database
    DATABASE_PATH = BASE_DIR / 'database' / 'heritage.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    AUDIO_FOLDER = BASE_DIR / 'static' / 'audio'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg'}
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'te': 'Telugu',
        'ta': 'Tamil',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'gu': 'Gujarati'
    }
    
    # AI Configuration (for Phase 2)
    OLLAMA_BASE_URL = 'http://localhost:11434'
    LLAMA_MODEL = 'llama2'
    STORY_MAX_LENGTH = 300  # words
    
    # Audio Configuration (for Phase 3)
    TTS_SAMPLE_RATE = 22050
    AUDIO_BITRATE = '64k'
    
    # Translation Configuration (for Phase 4)
    TRANSLATION_CACHE_TTL = 86400  # 24 hours
    DEFAULT_LANGUAGE = 'en'
    ENABLE_TRANSLATION_CACHE = True
    
    # Cache settings
    CACHE_STORIES = True
    CACHE_TIMEOUT = 86400  # 24 hours in seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

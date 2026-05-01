"""
Text-to-Speech Service using gTTS (Google Text-to-Speech)
Converts story text into audio narration
"""

import os
import hashlib
from pathlib import Path
from config import Config

class TTSService:
    """Service for converting text to speech"""
    
    def __init__(self):
        self.audio_folder = Config.AUDIO_FOLDER
        self.sample_rate = Config.TTS_SAMPLE_RATE
        self._initialized = False
        
        # Ensure audio folder exists
        os.makedirs(self.audio_folder, exist_ok=True)
    
    def initialize(self):
        """Initialize TTS (check if gTTS is available)"""
        if self._initialized:
            return True
        
        try:
            from gtts import gTTS
            self._initialized = True
            print("✅ gTTS (Google Text-to-Speech) ready!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing gTTS: {e}")
            return False
    
    def generate_audio(self, text, language='en', monument_name=''):
        """
        Generate audio from text using Google Text-to-Speech
        
        Args:
            text: Story text to convert to speech
            language: Language code (en, hi, te, ta, bn, mr, gu)
            monument_name: Monument name for filename
        
        Returns:
            Audio filename if successful, None if failed
        """
        try:
            from gtts import gTTS
            
            # Initialize if not already done
            if not self._initialized:
                if not self.initialize():
                    return None
            
            # Generate unique filename based on text hash
            text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
            filename = f"{monument_name.replace(' ', '_')}_{language}_{text_hash}.mp3"
            filepath = os.path.join(self.audio_folder, filename)
            
            # Check if audio already exists
            if os.path.exists(filepath):
                print(f"✅ Audio already exists: {filename}")
                return filename
            
            # Generate audio
            print(f"🎵 Generating audio for {monument_name}...")
            
            # Map language codes to gTTS supported languages
            lang_map = {
                'en': 'en',
                'hi': 'hi',
                'te': 'te',
                'ta': 'ta',
                'bn': 'bn',
                'mr': 'mr',
                'gu': 'gu'
            }
            
            gtts_lang = lang_map.get(language, 'en')
            
            # Create gTTS object
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
            
            # Save to file
            tts.save(filepath)
            
            print(f"✅ Audio generated: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return None
    
    def get_audio_duration(self, filename):
        """Get duration of audio file in seconds"""
        try:
            from pydub import AudioSegment
            
            filepath = os.path.join(self.audio_folder, filename)
            audio = AudioSegment.from_file(filepath)
            return len(audio) / 1000.0  # Convert to seconds
            
        except Exception as e:
            print(f"Error getting audio duration: {e}")
            return None
    
    def delete_audio(self, filename):
        """Delete audio file"""
        try:
            filepath = os.path.join(self.audio_folder, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting audio: {e}")
            return False
    
    def check_tts_available(self):
        """Check if TTS service is available"""
        try:
            from gtts import gTTS
            return True, "gTTS (Google Text-to-Speech) is available"
        except ImportError:
            return False, "gTTS not installed. Run: pip install gTTS"
        except Exception as e:
            return False, f"gTTS error: {str(e)}"


# Singleton instance
tts_service = TTSService()

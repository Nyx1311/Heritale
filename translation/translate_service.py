"""
Translation Service using Google Translate
Translates English stories to Indian languages
"""

from googletrans import Translator
from config import Config

class TranslationService:
    """Service for translating text between languages"""
    
    def __init__(self):
        self.translator = Translator()
        self._cache = {}  # Simple in-memory cache
    
    def translate(self, text, target_lang='hi', source_lang='en'):
        """
        Translate text from source to target language
        
        Args:
            text: Source text to translate
            target_lang: Target language code (hi, te, ta, bn, mr, gu)
            source_lang: Source language code (default: en)
        
        Returns:
            Translated text string
        """
        # Don't translate if target is English
        if target_lang == 'en':
            return text
        
        # Check cache first
        cache_key = f"{source_lang}_{target_lang}_{hash(text)}"
        if cache_key in self._cache:
            print(f"✅ Using cached translation for {target_lang}")
            return self._cache[cache_key]
        
        try:
            print(f"🌍 Translating to {target_lang}...")
            
            # Perform translation
            result = self.translator.translate(
                text, 
                src=source_lang, 
                dest=target_lang
            )
            
            translated_text = result.text
            
            # Cache the result
            self._cache[cache_key] = translated_text
            
            print(f"✅ Translation to {target_lang} complete!")
            return translated_text
            
        except Exception as e:
            print(f"❌ Translation error for {target_lang}: {e}")
            print(f"⚠️  Falling back to English")
            return text  # Fallback to original text
    
    def translate_batch(self, texts, target_lang='hi', source_lang='en'):
        """
        Translate multiple texts at once
        
        Args:
            texts: List of text strings to translate
            target_lang: Target language code
            source_lang: Source language code
        
        Returns:
            List of translated texts
        """
        if target_lang == 'en':
            return texts
        
        try:
            results = []
            for text in texts:
                translated = self.translate(text, target_lang, source_lang)
                results.append(translated)
            return results
            
        except Exception as e:
            print(f"Batch translation error: {e}")
            return texts  # Fallback to original
    
    def get_language_name(self, lang_code):
        """Get full language name from code"""
        return Config.SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')
    
    def check_translation_available(self):
        """Check if translation service is working"""
        try:
            # Test translation
            test = self.translator.translate("Hello", src='en', dest='hi')
            if test and test.text:
                return True, "Google Translate is available"
            return False, "Translation test failed"
            
        except Exception as e:
            return False, f"Translation error: {str(e)}"
    
    def get_supported_languages(self):
        """Get list of supported language codes"""
        return list(Config.SUPPORTED_LANGUAGES.keys())


# Singleton instance
translation_service = TranslationService()

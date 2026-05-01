"""
LLaMA Story Generation Service
Interfaces with Ollama to generate heritage stories using LLaMA 3.2
"""

import requests
import json
from config import Config

class LLaMAService:
    """Service for generating stories using LLaMA via Ollama"""
    
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = "llama3.2"  # Using llama 3.2
        self.max_retries = 3
    
    def generate_story(self, monument_name, monument_description, user_stories=None, language='en'):
        """
        Generate a narrative story about a monument
        
        Args:
            monument_name: Name of the monument
            monument_description: Official historical description
            user_stories: List of community-contributed stories (optional)
            language: Target language code (default: 'en')
        
        Returns:
            Generated story text or None if failed
        """
        try:
            # Build the prompt
            prompt = self._build_prompt(monument_name, monument_description, user_stories, language)
            
            # Call Ollama API
            response = self._call_ollama(prompt)
            
            if response:
                # Clean and format the response
                story = self._clean_story(response)
                return story
            
            return None
            
        except Exception as e:
            print(f"Error generating story: {e}")
            return None
    
    def _build_prompt(self, monument_name, monument_description, user_stories, language):
        """Build the story generation prompt"""
        
        # Base prompt with role and style instructions
        prompt = f"""You are a masterful storyteller preserving Indian heritage through enchanting narratives.

Your task is to create a captivating story about {monument_name} in a classic storytelling style.

STORYTELLING STYLE:
- Begin with phrases like "Once upon a time...", "Long ago...", "In the heart of...", "There once stood...", or "Centuries ago..."
- Write as a flowing narrative with a beginning, middle, and end
- Use vivid, poetic imagery and emotional language
- Create a sense of wonder and magic around the monument's history
- Make readers feel like they're listening to a grandmother's tale by the fireside
- Weave historical facts into the narrative naturally, not as dry information
- Include sensory details: sounds, sights, textures, atmosphere
- Use dramatic elements: mystery, grandeur, human emotions, turning points
- Keep it around 300-350 words
- Write in past tense initially, then transition to present for lasting impact

HISTORICAL FOUNDATION:
{monument_description}
"""
        
        # Add community stories if available
        if user_stories and len(user_stories) > 0:
            prompt += "\n\nVOICES FROM VISITORS (weave these memories naturally into your story):\n"
            for idx, story in enumerate(user_stories[:5], 1):  # Max 5 stories
                story_text = story.get('translated_english_text') or story.get('user_text', '')
                if story_text and story_text.strip() and not story_text.startswith('['):
                    prompt += f"{idx}. {story_text}\n"
        
        # Language-specific instruction
        if language != 'en':
            language_names = {
                'hi': 'Hindi',
                'te': 'Telugu',
                'ta': 'Tamil',
                'bn': 'Bengali',
                'mr': 'Marathi',
                'gu': 'Gujarati'
            }
            lang_name = language_names.get(language, 'English')
            prompt += f"\n\nIMPORTANT: Write the entire story in {lang_name} using traditional storytelling phrases and style natural to {lang_name} culture.\n"
        
        prompt += f"""

Now create an enchanting narrative story about {monument_name}. 
- Start with a classic storytelling opening
- Paint vivid scenes with your words
- Make the monument come alive with drama and emotion
- End with a reflection on its lasting significance

Begin directly with your story - no titles or introductions needed."""
        
        return prompt
    
    def _call_ollama(self, prompt):
        """Make API call to Ollama"""
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,  # Balance creativity and coherence
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 400  # Max tokens for response
                }
            }
            
            print(f"Calling Ollama API with model: {self.model}")
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            story_text = result.get('response', '')
            
            return story_text
            
        except requests.exceptions.Timeout:
            print("Ollama API timeout - story generation took too long")
            return None
        except requests.exceptions.ConnectionError:
            print("Cannot connect to Ollama. Make sure Ollama is running (ollama serve)")
            return None
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return None
    
    def _clean_story(self, story_text):
        """Clean and format the generated story"""
        # Remove any markdown formatting
        story = story_text.strip()
        
        # Remove common prefixes that LLaMA might add
        prefixes_to_remove = [
            "Here is the story:",
            "Here's the story:",
            "Story:",
            "The story:",
        ]
        
        for prefix in prefixes_to_remove:
            if story.lower().startswith(prefix.lower()):
                story = story[len(prefix):].strip()
        
        # Ensure it's not too short
        if len(story) < 100:
            return None
        
        return story
    
    def check_ollama_status(self):
        """Check if Ollama is running and accessible"""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [m.get('name', '') for m in models]
                print(f"Ollama is running. Available models: {available_models}")
                
                # Check if llama3.2 is available
                if any('llama3.2' in model.lower() or 'llama3:' in model.lower() for model in available_models):
                    return True, "LLaMA 3.2 is available"
                else:
                    return False, f"LLaMA 3.2 not found. Available: {available_models}"
            
            return False, "Ollama not responding"
            
        except Exception as e:
            return False, f"Cannot connect to Ollama: {e}"


# Singleton instance
llama_service = LLaMAService()

from flask import Blueprint, jsonify, request
from database.db import db_session
from database.models import Monument, UserStory, GeneratedStory
from ai.llama_service import llama_service
from audio.tts_service import tts_service
from translation.translate_service import translation_service
from datetime import datetime
import threading

story_bp = Blueprint('stories', __name__)

@story_bp.route('/story/<int:monument_id>', methods=['GET'])
def generate_story(monument_id):
    """Generate or retrieve story for a monument"""
    try:
        language = request.args.get('language', 'en')
        force_regenerate = request.args.get('regenerate', 'false').lower() == 'true'
        
        # Get monument
        monument = Monument.query.get(monument_id)
        if not monument:
            return jsonify({
                'success': False,
                'error': 'Monument not found'
            }), 404
        
        # Check if story already exists in cache (unless force regenerate)
        if not force_regenerate:
            existing_story = GeneratedStory.query.filter_by(
                monument_id=monument_id,
                language=language
            ).first()
            
            if existing_story:
                # Increment play count
                existing_story.play_count += 1
                db_session.commit()
                
                return jsonify({
                    'success': True,
                    'story': existing_story.to_dict(),
                    'monument': monument.to_dict(),
                    'cached': True
                })
        
        # Get approved user stories for context
        user_stories = UserStory.query.filter_by(
            monument_id=monument_id,
            is_approved=1
        ).order_by(UserStory.created_at.desc()).limit(5).all()
        
        user_stories_data = [story.to_dict() for story in user_stories]
        
        # Generate story using LLaMA (always in English first)
        print(f"Generating AI story for {monument.name}...")
        story_text = llama_service.generate_story(
            monument_name=monument.name,
            monument_description=monument.official_description,
            user_stories=user_stories_data,
            language='en'  # Always generate in English first
        )
        
        if not story_text:
            # Fallback to a basic description if AI generation fails
            return jsonify({
                'success': False,
                'error': 'AI story generation failed. Please ensure Ollama is running with llama3.2',
                'fallback': monument.official_description[:300] + "..."
            }), 500
        
        # Translate story if needed (Phase 4)
        if language != 'en':
            print(f"🌍 Translating story to {language}...")
            story_text = translation_service.translate(
                text=story_text,
                target_lang=language,
                source_lang='en'
            )
        
        # Generate audio from story text (Phase 3)
        print(f"🎵 Generating audio for {monument.name} in {language}...")
        audio_filename = tts_service.generate_audio(
            text=story_text,
            language=language,
            monument_name=monument.name
        )
        
        if audio_filename:
            print(f"✅ Audio generated: {audio_filename}")
        else:
            print("⚠️  Audio generation failed, story will be text-only")
        
        # Save generated story to database
        generated_story = GeneratedStory(
            monument_id=monument_id,
            language=language,
            story_text=story_text,
            audio_path=audio_filename,  # Now includes audio!
            play_count=1,
            generated_at=datetime.utcnow()
        )
        
        db_session.add(generated_story)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'story': generated_story.to_dict(),
            'monument': monument.to_dict(),
            'cached': False,
            'user_stories_included': len(user_stories_data),
            'audio_generated': audio_filename is not None
        })
    
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@story_bp.route('/story/<int:story_id>', methods=['GET'])
def get_story(story_id):
    """Get a specific generated story"""
    try:
        story = GeneratedStory.query.get(story_id)
        
        if not story:
            return jsonify({
                'success': False,
                'error': 'Story not found'
            }), 404
        
        return jsonify({
            'success': True,
            'story': story.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@story_bp.route('/stories/monument/<int:monument_id>', methods=['GET'])
def get_monument_stories(monument_id):
    """Get all stories for a monument"""
    try:
        stories = GeneratedStory.query.filter_by(monument_id=monument_id).all()
        
        return jsonify({
            'success': True,
            'stories': [story.to_dict() for story in stories],
            'count': len(stories)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@story_bp.route('/ai/status', methods=['GET'])
def check_ai_status():
    """Check if AI service (Ollama) is available"""
    try:
        is_available, message = llama_service.check_ollama_status()
        
        return jsonify({
            'success': is_available,
            'message': message,
            'model': llama_service.model,
            'base_url': llama_service.base_url
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@story_bp.route('/tts/status', methods=['GET'])
def check_tts_status():
    """Check if TTS service is available"""
    try:
        is_available, message = tts_service.check_tts_available()
        
        return jsonify({
            'success': is_available,
            'message': message
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@story_bp.route('/translation/status', methods=['GET'])
def check_translation_status():
    """Check if translation service is available"""
    try:
        is_available, message = translation_service.check_translation_available()
        
        return jsonify({
            'success': is_available,
            'message': message,
            'supported_languages': translation_service.get_supported_languages()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

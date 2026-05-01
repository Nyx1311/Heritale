from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from database.db import db_session
from database.models import UserStory, Monument
from translation.translate_service import translation_service
import os
from config import Config

user_input_bp = Blueprint('user_input', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_AUDIO_EXTENSIONS


@user_input_bp.route('/upload/text', methods=['POST'])
def upload_text_story():
    """Accept text story submission from user"""
    try:
        data = request.get_json()
        
        monument_id = data.get('monument_id')
        user_text = data.get('user_text')
        
        if not monument_id or not user_text:
            return jsonify({
                'success': False,
                'error': 'monument_id and user_text are required'
            }), 400
        
        # Verify monument exists
        monument = Monument.query.get(monument_id)
        if not monument:
            return jsonify({
                'success': False,
                'error': 'Monument not found'
            }), 404
        
        # Detect language and translate to English if needed (Phase 4 & 5)
        detected_language = data.get('language', 'en')  # Get language from request
        translated_text = user_text
        
        # If not English, translate to English for AI context
        if detected_language != 'en':
            try:
                translated_text = translation_service.translate(
                    user_text, 
                    target_lang='en', 
                    source_lang=detected_language
                )
                print(f"✅ Translated user story from {detected_language} to English")
            except Exception as e:
                print(f"⚠️ Translation failed: {e}. Using original text.")
                translated_text = user_text
        
        # Create user story
        user_story = UserStory(
            monument_id=monument_id,
            user_text=user_text,
            detected_language=detected_language,
            translated_english_text=translated_text,
            is_approved=0  # Pending approval
        )
        
        db_session.add(user_story)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Story submitted successfully',
            'story': user_story.to_dict()
        })
    
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_input_bp.route('/upload/audio', methods=['POST'])
def upload_audio_story():
    """Accept audio story submission from user"""
    try:
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        monument_id = request.form.get('monument_id')
        
        if not monument_id:
            return jsonify({
                'success': False,
                'error': 'monument_id is required'
            }), 400
        
        # Verify monument exists
        monument = Monument.query.get(monument_id)
        if not monument:
            return jsonify({
                'success': False,
                'error': 'Monument not found'
            }), 404
        
        if audio_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            
            # Create unique filename
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            
            # Save file
            audio_file.save(filepath)
            
            # Create user story (Phase 5 will add STT processing)
            user_story = UserStory(
                monument_id=monument_id,
                user_audio_path=unique_filename,
                user_text='[Audio transcription pending - Phase 5]',
                detected_language='unknown',
                translated_english_text='[Translation pending - Phase 5]',
                is_approved=0
            )
            
            db_session.add(user_story)
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Audio submitted successfully',
                'story': user_story.to_dict(),
                'note': 'Audio transcription will be added in Phase 5'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed: mp3, wav, m4a, ogg'
            }), 400
    
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_input_bp.route('/user-stories/<int:monument_id>', methods=['GET'])
def get_user_stories(monument_id):
    """Get all user stories for a monument (approved and recent pending ones)"""
    try:
        # Get approved stories + recent pending ones (last 24 hours)
        from datetime import datetime, timedelta
        recent_time = datetime.utcnow() - timedelta(hours=24)
        
        stories = UserStory.query.filter(
            UserStory.monument_id == monument_id
        ).filter(
            (UserStory.is_approved == 1) | 
            ((UserStory.is_approved == 0) & (UserStory.created_at >= recent_time))
        ).order_by(UserStory.created_at.desc()).limit(20).all()
        
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

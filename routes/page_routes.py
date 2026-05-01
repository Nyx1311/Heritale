# Story page route - serves the story.html template
from flask import render_template, request
from app import app

@app.route('/story')
def story_page():
    """Serve the story page"""
    monument_id = request.args.get('monument_id')
    language = request.args.get('language', 'en')
    
    return render_template('story.html', monument_id=monument_id, language=language)

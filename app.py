from flask import Flask, render_template, jsonify
from flask_cors import CORS
from config import config
from database.db import db_session, init_db, close_db
import os

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register teardown function
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db()
    
    # Register blueprints
    from routes.monument_routes import monument_bp
    from routes.story_routes import story_bp
    from routes.user_input_routes import user_input_bp
    
    app.register_blueprint(monument_bp, url_prefix='/api')
    app.register_blueprint(story_bp, url_prefix='/api')
    app.register_blueprint(user_input_bp, url_prefix='/api')
    
    # Home route
    @app.route('/')
    def index():
        """Main page with India map"""
        return render_template('index.html')
    
    # Story page route
    @app.route('/story')
    def story_page():
        """Serve the story page"""
        return render_template('story.html')
    
    # Health check
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'AI Heritage Storyteller is running'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

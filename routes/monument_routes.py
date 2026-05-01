from flask import Blueprint, jsonify, request
from database.db import db_session
from database.models import Monument
from services.image_service import image_service

monument_bp = Blueprint('monuments', __name__)

@monument_bp.route('/states', methods=['GET'])
def get_states():
    """Get list of all states with monuments and their counts"""
    try:
        from sqlalchemy import func
        
        # Query states with monument counts
        states_with_counts = db_session.query(
            Monument.state,
            func.count(Monument.id).label('count')
        ).group_by(Monument.state).order_by(Monument.state).all()
        
        state_list = [{'state': state, 'count': count} for state, count in states_with_counts]
        
        return jsonify({
            'success': True,
            'states': state_list,
            'count': len(state_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monument_bp.route('/monuments/<state>', methods=['GET'])
def get_monuments_by_state(state):
    """Get all monuments in a specific state"""
    try:
        monuments = Monument.query.filter_by(state=state).all()
        
        if not monuments:
            return jsonify({
                'success': True,
                'monuments': [],
                'message': f'No monuments found for {state}'
            })
        
        monuments_list = [monument.to_dict() for monument in monuments]
        
        return jsonify({
            'success': True,
            'state': state,
            'monuments': monuments_list,
            'count': len(monuments_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monument_bp.route('/monument/<int:monument_id>', methods=['GET'])
def get_monument(monument_id):
    """Get single monument details"""
    try:
        monument = Monument.query.get(monument_id)
        
        if not monument:
            return jsonify({
                'success': False,
                'error': 'Monument not found'
            }), 404
        
        return jsonify({
            'success': True,
            'monument': monument.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monument_bp.route('/monuments', methods=['GET'])
def get_all_monuments():
    """Get all monuments (with optional pagination)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        monuments = Monument.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'monuments': [m.to_dict() for m in monuments.items],
            'total': monuments.total,
            'page': page,
            'pages': monuments.pages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monument_bp.route('/monument/<int:monument_id>/image', methods=['GET'])
def get_monument_image(monument_id):
    """Get image URL for a specific monument"""
    try:
        monument = Monument.query.get(monument_id)
        
        if not monument:
            return jsonify({
                'success': False,
                'error': 'Monument not found'
            }), 404
        
        # Fetch image from Wikipedia
        image_url = image_service.get_monument_image(monument.name, monument.state)
        
        return jsonify({
            'success': True,
            'monument_id': monument_id,
            'image_url': image_url
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monument_bp.route('/monument/<int:monument_id>/gallery', methods=['GET'])
def get_monument_gallery(monument_id):
    """Get multiple images for a monument gallery"""
    try:
        monument = Monument.query.get(monument_id)
        
        if not monument:
            return jsonify({
                'success': False,
                'error': 'Monument not found'
            }), 404
        
        # Fetch multiple images from Wikipedia
        limit = request.args.get('limit', 6, type=int)
        image_urls = image_service.get_monument_images_gallery(monument.name, monument.state, limit)
        
        return jsonify({
            'success': True,
            'monument_id': monument_id,
            'images': image_urls
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

from flask import Blueprint, jsonify, send_from_directory, current_app
import os
from app.controllers.team_controller import get_team_members

team_bp = Blueprint('team', __name__)

@team_bp.route('/api/team', methods=['GET'])
def get_team():
    """Hämta alla teammedlemmar."""
    team_members = get_team_members()
    return jsonify(team_members)

@team_bp.route('/static/images/<path:filename>')
def serve_image(filename):
    """Servera bilder från den externa static/images-mappen."""
    static_folder = os.path.join(current_app.root_path, '..', 'static', 'images')
    return send_from_directory(static_folder, filename)


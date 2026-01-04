from flask import Blueprint
from src.controllers.pdf_controller import generate_pdf, health_check, get_pdf_stats

api_bp = Blueprint('api', __name__)

api_bp.route('/health', methods=['GET'])(health_check)
api_bp.route('/stats', methods=['GET'])(get_pdf_stats)
api_bp.route('/generate-pdf', methods=['POST'])(generate_pdf)

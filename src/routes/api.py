from flask import Blueprint
from src.controllers.pdf_controller import generate_pdf, health_check, get_pdf_stats
from src.extensions import limiter

api_bp = Blueprint('api', __name__)

api_bp.route('/health', methods=['GET'])(health_check)

@api_bp.route('/stats', methods=['GET'])
@limiter.limit("30 per minute")
def stats_route():
    return get_pdf_stats()

@api_bp.route('/generate-pdf', methods=['POST'])
@limiter.limit("10 per minute")
def generate_pdf_route():
    return generate_pdf()

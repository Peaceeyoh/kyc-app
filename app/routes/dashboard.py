from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    return "<h1>KYC compliance system</h1> <p>System is running</p>"


@dashboard_bp.route('/health')
def health_check():
    return {'status': 'healthy', 'system': 'KYC Compliance App'}
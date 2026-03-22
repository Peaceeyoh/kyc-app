from flask import Blueprint
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    return f'''
        <h1>KYC Compliance System</h1>
        <p>Welcome, {current_user.username}!</p>
        <p>Role: {current_user.role}</p>
        <a href="/auth/logout">Logout</a>
    '''


@dashboard_bp.route('/health')
def health_check():
    return {'status': 'healthy', 'system': 'KYC Compliance App'}
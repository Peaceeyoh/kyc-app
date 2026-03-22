from flask import Blueprint, redirect, url_for, flash, render_template_string
from flask_dance.contrib.github import make_github_blueprint, github
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
import os

auth_bp = Blueprint('auth', __name__)

github_bp = make_github_blueprint(
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    redirect_to='auth.github_callback'
)


@auth_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>KYC Compliance - Login</title>
            <style>
                body { font-family: Arial, sans-serif; display: flex;
                       justify-content: center; align-items: center;
                       height: 100vh; margin: 0; background: #f5f5f5; }
                .card { background: white; padding: 40px; border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                h1 { color: #333; margin-bottom: 8px; }
                p { color: #666; margin-bottom: 24px; }
                a { background: #24292e; color: white; padding: 12px 24px;
                    border-radius: 6px; text-decoration: none; font-size: 16px; }
                a:hover { background: #444; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>KYC Compliance System</h1>
                <p>Sign in to access the compliance dashboard</p>
                <a href="/auth/github/authorized">Login with GitHub</a>
            </div>
        </body>
        </html>
    ''')


@auth_bp.route('/github/authorized')
def github_callback():
    if not github.authorized:
        return redirect(url_for('github.login'))

    resp = github.get('/user')
    if not resp.ok:
        flash('Failed to fetch user info from GitHub')
        return redirect(url_for('auth.login'))

    github_info = resp.json()
    github_id = str(github_info['id'])
    username = github_info['login']
    email = github_info.get('email', '')

    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        user = User(
            github_id=github_id,
            username=username,
            email=email
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('dashboard.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
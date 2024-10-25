from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/manage-users')
@login_required
def manage_users():
    return render_template('admin/manage_users.html')

# Add routes for user management, reports, etc.

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('parent/dashboard.html')

# Add routes for viewing child progress, fees, etc.

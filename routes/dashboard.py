from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Scan

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    recent_scans = Scan.query.filter_by(user_id=current_user.id)\
                     .order_by(Scan.created_at.desc())\
                     .limit(5).all()
    return render_template('dashboard/index.html', scans=recent_scans)

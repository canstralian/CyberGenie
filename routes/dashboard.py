from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from models import Scan

bp = Blueprint('dashboard', __name__)

@bp.before_request
@login_required
def before_request():
    """
    Ensure the user is logged in before processing any request.
    """
    pass

@bp.route('/')
@bp.route('/dashboard')
def index():
    """
    Render the dashboard index page with recent scans and pagination.

    Returns:
        Response: The rendered template for the dashboard index page.
    """
    page = request.args.get('page', 1, type=int)
    scans_per_page = 5
    pagination = (
        Scan.query.filter_by(user_id=current_user.id)
        .order_by(Scan.created_at.desc())
        .paginate(page, scans_per_page, False)
    )
    recent_scans = pagination.items
    if not recent_scans:
        flash('No recent scans found.')
    total_scans = Scan.query.filter_by(user_id=current_user.id).count()
    return render_template(
        'dashboard/index.html',
        scans=recent_scans,
        pagination=pagination,
        total_scans=total_scans,
    )

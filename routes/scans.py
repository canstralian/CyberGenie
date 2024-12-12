from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Scan, Finding
from services import snowflake_service, mistral_service, ml_service

bp = Blueprint('scans', __name__)

@bp.route('/scans')
@login_required
def list_scans():
    scans = Scan.query.filter_by(user_id=current_user.id).all()
    return render_template('scans/list.html', scans=scans)

@bp.route('/scans/<int:scan_id>')
@login_required
def scan_detail(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        abort(403)
    return render_template('scans/detail.html', scan=scan)

@bp.route('/scans/new', methods=['POST'])
@login_required
def create_scan():
    target_url = request.form.get('target_url')
    scan = Scan(target_url=target_url, user_id=current_user.id)
    db.session.add(scan)
    db.session.commit()
    
    # Start async scan process
    mistral_service.start_scan_workflow(scan.id)
    
    return jsonify({'status': 'success', 'scan_id': scan.id})

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db
from models import Scan, Finding
from services.scan_service import ScanService
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('scans', __name__, url_prefix='/scans')
scan_service = ScanService()

@bp.route('/')
@login_required
def list_scans():
    scans = Scan.query.filter_by(user_id=current_user.id).all()
    return render_template('scans/list.html', scans=scans)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_scan():
    if request.method == 'POST':
        target_url = request.form.get('target_url')
        scan_type = request.form.get('scan_type', 'basic')
        error_message = None
        
        try:
            # Create scan record in database
            result = scan_service.start_scan(target_url, scan_type)
            logger.info(f"Scan started successfully: {result}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'status': 'success', 'scan_id': result['scan_id']})
            
            flash('Scan started successfully!', 'success')
            return redirect(url_for('scans.scan_detail', scan_id=result['scan_id']))
            
        except ValueError as e:
            # Handle validation errors with specific messages
            error_message = str(e)
            logger.warning(f"Validation error in scan creation: {error_message}")
            flash(error_message, 'warning')
        except Exception as e:
            # Handle other errors
            error_message = str(e)
            logger.error(f"Failed to start scan: {error_message}")
            flash('An unexpected error occurred while starting the scan. Please try again.', 'error')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'error',
                'message': error_message or 'An unexpected error occurred'
            }), 400
            
        return render_template('scans/new.html')
    
    return render_template('scans/new.html')

@bp.route('/<int:scan_id>')
@login_required
def scan_detail(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        abort(403)
    return render_template('scans/detail.html', scan=scan)

@bp.route('/<int:scan_id>/status')
@login_required
def scan_status(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        abort(403)
    return jsonify({
        'status': scan.status,
        'progress': 100 if scan.status == 'completed' else 50
    })

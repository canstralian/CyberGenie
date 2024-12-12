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
        
        try:
            try:
                result = scan_service.start_scan(target_url, scan_type)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'status': 'success',
                        'scan_id': result['scan_id'],
                        'message': 'Scan initiated successfully'
                    })
                
                flash('Scan started successfully! Please wait while we analyze the target.', 'success')
                return redirect(url_for('scans.scan_detail', scan_id=result['scan_id']))
            except Exception as e:
                logger.error(f"Scan initiation error: {str(e)}", exc_info=True)
                error_message = "Failed to start scan. Please try again or contact support if the issue persists."
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'status': 'error',
                        'message': error_message
                    }), 500
                
                flash(error_message, 'error')
                return redirect(url_for('scans.new'))
            
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            flash(str(e), 'warning')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 400
                
        except Exception as e:
            error_msg = "An unexpected error occurred. Please try again."
            logger.error(f"Scan error: {str(e)}")
            flash(error_msg, 'error')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': error_msg
                }), 500
    
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

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db, limiter
from models import Scan, Finding
from services.scan_service import ScanService
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('scans', __name__, url_prefix='/scans')
scan_service = ScanService()

@bp.route('/new', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
@login_required
@csrf.exempt  # Exempt CSRF for AJAX requests
def new_scan():
    form = ScanForm()
    if form.validate_on_submit():
        target_url = form.target_url.data
        scan_type = form.scan_type.data

        if scan_service.is_scan_running(target_url):
            flash(f"Scan for {target_url} is already running.", 'warning')
            return redirect(url_for('scans.new'))

        try:
            result = run_scan.apply_async(args=[target_url, scan_type])
            scan = Scan(target_url=target_url, scan_type=scan_type, status='queued', user_id=current_user.id)
            db.session.add(scan)
            db.session.commit()

            if request.is_xhr:
                return jsonify({'status': 'success', 'scan_id': scan.id, 'message': 'Scan initiated successfully'})

            flash('Scan started successfully! Please wait while we analyze the target.', 'success')
            return redirect(url_for('scans.scan_detail', scan_id=scan.id))

        except Exception as e:
            logger.error(f"Scan initiation error: {str(e)}", exc_info=True)
            error_message = "Failed to start scan. Please try again or contact support if the issue persists."

            if request.is_xhr:
                return jsonify({'status': 'error', 'message': error_message}), 500

            flash(error_message, 'error')
            return redirect(url_for('scans.new'))

    return render_template('scans/new.html', form=form)
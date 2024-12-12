import logging
from typing import Dict, List, Optional
import requests
from datetime import datetime
from app import db
from models import Scan, Finding

logger = logging.getLogger(__name__)

class ScanService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def start_scan(self, target_url: str, scan_type: str) -> Dict:
        """
        Start a new security scan
        """
        try:
            self.logger.info(f"Starting {scan_type} scan for {target_url}")
            
            # Validate URL
            if not target_url.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL format. URL must start with http:// or https://")
            
            # Basic reachability check
            try:
                response = requests.head(target_url, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error accessing target URL: {str(e)}")
                raise ValueError(f"Failed to access target URL: {str(e)}")
            
            # Create new scan record
            scan = Scan(
                target_url=target_url,
                status='pending',
                user_id=self._get_current_user_id()
            )
            
            try:
                db.session.add(scan)
                db.session.commit()
                
                return {
                    'status': 'started',
                    'scan_id': scan.id,
                    'target_url': target_url,
                    'scan_type': scan_type,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                db.session.rollback()
                self.logger.error(f"Database error creating scan: {str(e)}")
                raise Exception("Failed to create scan record")
            
        except ValueError as e:
            # Re-raise validation errors
            raise
        except Exception as e:
            self.logger.error(f"Error starting scan: {str(e)}")
            raise Exception(f"Failed to start scan: {str(e)}")
    
    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format and basic security checks
        """
    def _get_current_user_id(self):
        """Get current user ID from Flask-Login"""
        from flask_login import current_user
        if not current_user or not current_user.is_authenticated:
            raise ValueError("User must be authenticated to start a scan")
        return current_user.id

        if not url:
            return False
        
        if not url.startswith(('http://', 'https://')):
            return False
            
        # Add more validation as needed
        return True

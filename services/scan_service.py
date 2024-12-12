import logging
from datetime import datetime
import requests
from urllib.parse import urlparse, unquote
from flask import current_app
from app import db
from models import Scan

class ScanService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def start_scan(self, target_url, scan_type='basic'):
        """
        Start a new vulnerability scan for the given target URL
        """
        try:
            # Clean and validate URL
            cleaned_url = self._clean_url(target_url)
            if not self.validate_url(cleaned_url):
                raise ValueError("Invalid target URL format. Please provide a valid HTTP/HTTPS URL.")
            
            # Test URL accessibility
            try:
                response = requests.head(cleaned_url, timeout=10, allow_redirects=True, 
                                    headers={'User-Agent': 'Bug Hunter Scanner/1.0'})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error accessing target URL: {str(e)}")
                raise ValueError(f"Could not access the target URL. Please verify the URL is accessible and try again.")
            
            # Create new scan record
            scan = Scan(
                target_url=cleaned_url,
                status='pending',
                user_id=self._get_current_user_id()
            )
            
            try:
                db.session.add(scan)
                db.session.commit()
                
                self.logger.info(f"Starting {scan_type} scan for {cleaned_url}")
                
                return {
                    'status': 'started',
                    'scan_id': scan.id,
                    'target_url': cleaned_url,
                    'scan_type': scan_type,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                db.session.rollback()
                self.logger.error(f"Database error creating scan: {str(e)}")
                raise Exception("An internal error occurred while creating the scan. Please try again.")
            
        except ValueError as e:
            # Re-raise validation errors with user-friendly messages
            raise
        except Exception as e:
            # Log and re-raise other errors with a generic message
            self.logger.error(f"Error starting scan: {str(e)}")
            raise ValueError("An unexpected error occurred while starting the scan. Please try again.")

    def _clean_url(self, url):
        """
        Clean and normalize the URL
        """
        if not url:
            return ""
            
        # Remove any whitespace and decode URL
        cleaned = unquote(url.strip())
        
        # Ensure URL starts with http:// or https://
        if not cleaned.startswith(('http://', 'https://')):
            cleaned = 'https://' + cleaned
            
        return cleaned

    def validate_url(self, url):
        """
        Validate URL format and basic security checks
        """
        if not url:
            return False
            
        try:
            result = urlparse(url)
            return all([
                result.scheme in ['http', 'https'],
                result.netloc,
                not any(c in result.netloc for c in ['<', '>', '"', "'", '%']),
                len(url) <= 500
            ])
        except Exception:
            return False

    def _get_current_user_id(self):
        """Get current user ID from Flask-Login"""
        from flask_login import current_user
        if not current_user or not current_user.is_authenticated:
            raise ValueError("User must be authenticated to start a scan")
        return current_user.id

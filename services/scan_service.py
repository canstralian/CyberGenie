import logging
from datetime import datetime
import requests
from urllib.parse import urlparse, unquote
from flask import current_app
from flask_login import current_user
from app import db
from models import Scan

class ScanService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def start_scan(self, target_url, scan_type='basic'):
        """Start a new vulnerability scan for the given target URL"""
        if not target_url:
            raise ValueError("Target URL is required")

        if not current_user or not current_user.is_authenticated:
            raise ValueError("User must be authenticated to start a scan")

        try:
            # Clean and validate URL
            cleaned_url = self._clean_url(target_url)
            if not self._validate_url(cleaned_url):
                raise ValueError("Invalid target URL format. Please provide a valid HTTP/HTTPS URL.")
            
            # Test URL accessibility
            try:
                response = requests.head(
                    cleaned_url, 
                    timeout=30,
                    verify=False,  # Allow self-signed certificates
                    allow_redirects=True,
                    headers={
                        'User-Agent': 'Bug Hunter Scanner/1.0',
                        'Accept': '*/*'
                    }
                )
                # Don't raise for status, just log it
                if response.status_code >= 400:
                    self.logger.warning(f"Target URL returned status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Note: Target URL check warning: {str(e)}")
                # Continue anyway as the target might be intentionally blocking scanners
            
            # Create scan record
            scan = Scan(
                target_url=cleaned_url,
                status='pending',
                user_id=current_user.id
            )
            
            db.session.add(scan)
            db.session.commit()
            
            self.logger.info(f"Starting {scan_type} scan for {cleaned_url}")
            
            return {
                'status': 'success',
                'scan_id': scan.id,
                'target_url': cleaned_url,
                'scan_type': scan_type
            }

        except ValueError as e:
            # Re-raise validation errors
            raise
        except Exception as e:
            self.logger.error(f"Error starting scan: {str(e)}")
            db.session.rollback()
            raise ValueError("An unexpected error occurred while starting the scan.")

    def _clean_url(self, url):
        """Clean and normalize the URL"""
        if not url:
            return ""
        
        # Remove whitespace and decode URL
        cleaned = unquote(url.strip())
        
        # Ensure URL starts with http:// or https://
        if not cleaned.startswith(('http://', 'https://')):
            cleaned = 'https://' + cleaned
            
        return cleaned

    def _validate_url(self, url):
        """Validate URL format and basic security checks"""
        if not url:
            return False
            
        try:
            result = urlparse(url)
            return all([
                result.scheme in ['http', 'https'],
                result.netloc,
                # Basic security checks
                not any(c in result.netloc for c in ['<', '>', '"', "'", '%']),
                len(url) <= 500
            ])
        except Exception:
            return False

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
        """
        Initializes the ScanService with a logger for the class. 
        The logger will be used for logging information and errors related to scan operations.
        """
        self.logger = logging.getLogger(__name__)

    def start_scan(self, target_url, scan_type='basic'):
        """
        Starts a new vulnerability scan for the given target URL.

        Args:
            target_url (str): The URL to be scanned.
            scan_type (str): The type of scan to run (default is 'basic').

        Returns:
            dict: Contains the status of the scan initiation, the scan ID, target URL, and scan type.

        Raises:
            ValueError: If the URL is invalid, the user is not authenticated, or any unexpected error occurs.
        """
        # Check if target URL is provided
        if not target_url:
            self.logger.error("Target URL is required for the scan.")
            raise ValueError("Target URL is required")

        # Ensure user is authenticated
        if not current_user or not current_user.is_authenticated:
            self.logger.error("Unauthorized access attempt to start a scan.")
            raise ValueError("User must be authenticated to start a scan")

        try:
            # Clean and validate the target URL
            cleaned_url = self._clean_url(target_url)
            if not self._validate_url(cleaned_url):
                self.logger.error(f"Invalid target URL format: {cleaned_url}")
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
                # Log warnings if status code indicates potential issues
                if response.status_code >= 400:
                    self.logger.warning(f"Target URL returned status code {response.status_code} for {cleaned_url}")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Target URL check warning for {cleaned_url}: {str(e)}")
                # Proceed anyway as the target might be blocking scanners intentionally
            
            # Create a new scan record in the database
            scan = Scan(
                target_url=cleaned_url,
                status='pending',
                user_id=current_user.id
            )
            db.session.add(scan)
            db.session.commit()
            
            self.logger.info(f"Started {scan_type} scan for {cleaned_url}, Scan ID: {scan.id}")
            
            return {
                'status': 'success',
                'scan_id': scan.id,
                'target_url': cleaned_url,
                'scan_type': scan_type
            }

        except ValueError as e:
            # Re-raise validation errors to be handled elsewhere
            self.logger.error(f"Validation error during scan initiation: {str(e)}")
            raise
        except Exception as e:
            # Log unexpected errors and rollback the database session
            self.logger.error(f"Unexpected error during scan initiation: {str(e)}")
            db.session.rollback()
            raise ValueError("An unexpected error occurred while starting the scan.")

    def _clean_url(self, url):
        """
        Cleans and normalizes the URL by removing extra spaces and decoding it.

        Args:
            url (str): The target URL to clean.

        Returns:
            str: The cleaned URL.
        """
        if not url:
            self.logger.error("Provided URL is empty or None.")
            return ""
        
        # Remove any whitespace and decode the URL
        cleaned = unquote(url.strip())
        
        # Ensure the URL starts with either http:// or https://
        if not cleaned.startswith(('http://', 'https://')):
            cleaned = 'https://' + cleaned
            
        self.logger.debug(f"Cleaned URL: {cleaned}")
        return cleaned

    def _validate_url(self, url):
        """
        Validates the URL format, checks for common security risks, and ensures it follows basic URL standards.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        if not url:
            self.logger.error("URL is empty or None during validation.")
            return False
            
        try:
            result = urlparse(url)
            is_valid = all([
                result.scheme in ['http', 'https'],
                result.netloc,  # Ensure domain is present
                # Basic security checks to prevent certain dangerous characters in the domain
                not any(c in result.netloc for c in ['<', '>', '"', "'", '%']),
                len(url) <= 500  # Limit URL length for security
            ])
            self.logger.debug(f"URL validation result for {url}: {is_valid}")
            return is_valid
        except Exception as e:
            self.logger.error(f"Error during URL validation for {url}: {str(e)}")
            return False

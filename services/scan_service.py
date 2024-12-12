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
            
            # Create scan record
            scan = Scan.query.filter_by(target_url=target_url)\
                           .order_by(Scan.created_at.desc())\
                           .first()
            
            if scan and scan.status in ['pending', 'running']:
                raise ValueError("A scan is already in progress for this target")
            
            return {
                'status': 'started',
                'target_url': target_url,
                'scan_type': scan_type,
                'timestamp': datetime.now().isoformat()
            }
            
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
        if not url:
            return False
        
        if not url.startswith(('http://', 'https://')):
            return False
            
        # Add more validation as needed
        return True

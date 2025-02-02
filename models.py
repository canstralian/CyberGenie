"""
Models module for the application.
"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from app import db
from typing import List

# Initialize Bcrypt
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        scans (List[Scan]): The list of scans associated with the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    scans = db.relationship('Scan', back_populates='user', lazy=True)

    def set_password(self, password: str) -> None:
        """
        Hash the password and store it.

        Args:
            password (str): The plain text password to be hashed.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored hash.

        Args:
            password (str): The plain text password to be checked.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

class Scan(db.Model):
    """
    Represents a scan in the application.

    Attributes:
        id (int): The unique identifier for the scan.
        target_url (str): The target URL to be scanned.
        status (str): The status of the scan (e.g., pending, completed).
        created_at (datetime): The timestamp when the scan was created.
        completed_at (datetime): The timestamp when the scan was completed.
        findings (List[Finding]): The list of findings associated with the scan.
        user_id (int): The ID of the user who initiated the scan.
        user (User): The user who initiated the scan.
    """
    id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    findings = db.relationship('Finding', back_populates='scan', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='scans')

class Finding(db.Model):
    """
    Represents a finding in the application.

    Attributes:
        id (int): The unique identifier for the finding.
        vulnerability_type (str): The type of vulnerability found.
        severity (str): The severity level of the vulnerability.
        description (str): The description of the vulnerability.
        proof_of_concept (str): The proof of concept for the vulnerability.
        created_at (datetime): The timestamp when the finding was created.
        scan_id (int): The ID of the scan associated with the finding.
        scan (Scan): The scan associated with the finding.
    """
    id = db.Column(db.Integer, primary_key=True)
    vulnerability_type = db.Column(db.String(100))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    proof_of_concept = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)
    scan = db.relationship('Scan', back_populates='findings')

# Ensure file ends with a newline

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from typing import List

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    scans = db.relationship('Scan', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    findings = db.relationship('Finding', backref='scan', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Finding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vulnerability_type = db.Column(db.String(100))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    proof_of_concept = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)
    
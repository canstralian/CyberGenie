"""
Configuration module for the Flask application.
"""

import os

class Config:
    """
    Configuration class for setting up environment variables.
    """
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(24).hex())
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SNOWFLAKE_USER = os.environ.get("SNOWFLAKE_USER", os.environ.get("PGUSER"))
    SNOWFLAKE_PASSWORD = os.environ.get("SNOWFLAKE_PASSWORD", os.environ.get("PGPASSWORD"))
    SNOWFLAKE_ACCOUNT = os.environ.get("SNOWFLAKE_ACCOUNT", os.environ.get("PGHOST"))
    SNOWFLAKE_DATABASE = os.environ.get("SNOWFLAKE_DATABASE", os.environ.get("PGDATABASE"))
    SNOWFLAKE_PORT = os.environ.get("SNOWFLAKE_PORT", os.environ.get("PGPORT"))

    HUGGINGFACE_MODEL = "microsoft/codebert-base"
    DEBUG = True
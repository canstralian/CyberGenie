import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for setting up environment variables.
    """
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(24).hex())
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"
    # Add other configurations as needed

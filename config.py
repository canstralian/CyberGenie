import os

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(24).hex())
    # Use SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Snowflake Configuration
    SNOWFLAKE_USER = os.environ.get("SNOWFLAKE_USER", os.environ.get("PGUSER"))
    SNOWFLAKE_PASSWORD = os.environ.get("SNOWFLAKE_PASSWORD", os.environ.get("PGPASSWORD"))
    SNOWFLAKE_ACCOUNT = os.environ.get("SNOWFLAKE_ACCOUNT", os.environ.get("PGHOST"))
    SNOWFLAKE_DATABASE = os.environ.get("SNOWFLAKE_DATABASE", os.environ.get("PGDATABASE"))
    SNOWFLAKE_PORT = os.environ.get("SNOWFLAKE_PORT", os.environ.get("PGPORT"))

    # HuggingFace Configuration
    HUGGINGFACE_MODEL = "microsoft/codebert-base"
    
    # Debug mode
    DEBUG = True

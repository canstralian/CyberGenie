import os

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(24).hex())
    # Ensure DATABASE_URL starts with postgresql://
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = db_url
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

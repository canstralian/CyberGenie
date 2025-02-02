import logging
import sys
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    """
    Load user by ID.
    
    Args:
        id (int): User ID
    
    Returns:
        User: User object corresponding to the provided ID
    """
    from models import User
    return User.query.get(int(id))

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application
    """
    # Ensure the instance folder exists
    try:
        os.makedirs('instance')
    except OSError:
        pass
    logger.info("Creating Flask application...")
    app = Flask(__name__)
    
    # Load configuration
    logger.info("Loading configuration...")
    app.config.from_object(Config)
    
    # Initialize Flask extensions
    logger.info("Initializing Flask extensions...")
    try:
        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        logger.info("Flask extensions initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Flask extensions: {str(e)}")
        raise

    # Initialize blueprints and database
    try:
        with app.app_context():
            # Import routes
            logger.info("Registering blueprints...")
            from routes import auth, dashboard, scans
            app.register_blueprint(auth.bp)
            app.register_blueprint(dashboard.bp)
            app.register_blueprint(scans.bp)
            logger.info("Blueprints registered successfully")

            # Create database tables
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Error during app initialization: {str(e)}")
        raise

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """
        Handle 404 errors (Page not found).
        
        Args:
            error (HTTPException): The HTTP exception that triggered this handler
        
        Returns:
            tuple: A tuple containing the error message and the HTTP status code
        """
        logger.warning(f"Page not found: {request.url}")
        return "Page not found", 404

    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 errors (Internal server error).
        
        Args:
            error (HTTPException): The HTTP exception that triggered this handler
        
        Returns:
            tuple: A tuple containing the error message and the HTTP status code
        """
        logger.error(f"Server error: {error}")
        db.session.rollback()
        return "Internal server error", 500

    logger.info("Flask application created successfully")
    return app

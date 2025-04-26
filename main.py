import logging
import sys
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

try:
    logger.info("Initializing application...")
    app = create_app()
    logger.info("Application initialized successfully")

    if __name__ == "__main__":
        logger.info("Starting Flask server...")
        app.run(host="0.0.0.0", port=5000, debug=app.config['DEBUG'])
except RuntimeError as e:
    logger.error("Failed to start application: %s", e)
    sys.exit(1)

import os
import logging
from typing import Optional

from dotenv import load_dotenv
import gridfs

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from . import llm_modelling


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_URI = "mongodb://127.0.0.1:27017"
DEFAULT_DATABASE = "tanc_database"
DEFAULT_UPLOAD_FOLDER = '/cache'
SUPPORTED_MODELS = ["openai", "azure", "huggingface"]

# Global variables
client: Optional[MongoClient] = None
db = None
grid_fs = None



def validate_model_parameter(model: str) -> str:
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Model must be one of {SUPPORTED_MODELS}, got {model}")
    return model



def connect_to_mongodb(uri: str = DEFAULT_URI, database_name: str = DEFAULT_DATABASE) -> tuple[MongoClient, any]:
    """
    Connect to MongoDB with error handling.
    """
    global client, db
    try:
        logger.info(f"Attempting to connect to MongoDB at {uri}")
        # Validate URI
        if not uri or not isinstance(uri, str):
            raise ValueError(f"Invalid MongoDB URI: {uri}")
        # Create client with timeout
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        # Get or create database
        dbnames = client.list_database_names()
        if database_name in dbnames:
            logger.info(f"Using existing database: {database_name}")
            db = client[database_name]
        else:
            logger.info(f"Creating new database: {database_name}")
            db = client[database_name]
            # Initialize database with a collection
            init_col = db['init']
            init_col.insert_one({'text': 'init database'})
            logger.info("Database initialized successfully")
        return client, db
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise ConnectionFailure(f"Unable to connect to MongoDB at {uri}. Please ensure MongoDB is running.") from e
    except ServerSelectionTimeoutError as e:
        logger.error(f"MongoDB server selection timeout: {e}")
        raise ServerSelectionTimeoutError(f"MongoDB server at {uri} is not available. Please check if MongoDB is running.") from e
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise



def setup_gridfs(database) -> gridfs.GridFS:
    """
    Set up GridFS with error handling.
    """
    if database is None:
        raise ValueError("Database cannot be None for GridFS setup")
    try:
        logger.info("Setting up GridFS")
        grid_fs = gridfs.GridFS(database)
        logger.info("GridFS setup completed successfully")
        return grid_fs
    except Exception as e:
        logger.error(f"Failed to setup GridFS: {e}")
        raise



def setup_flask_app() -> Flask:
    """
    Set up Flask application with CORS.
    """
    try:
        logger.info("Creating Flask application")
        app = Flask(__name__)
        # Configure CORS
        logger.info("Configuring CORS")
        CORS(app, resources={r"/backend/*": {"origins": "*"}}, allow_headers="*", methods=["GET", "POST", "OPTIONS"])
        logger.info("Flask application created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to create Flask application: {e}")
        raise



def load_environment_variables() -> None:
    """
    Load environment variables from .env file.
    """
    try:
        logger.info("Loading environment variables from .env file")
        load_dotenv()
        logger.info("Environment variables loaded successfully")
    except FileNotFoundError:
        logger.warning(".env file not found. Using system environment variables.")
    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")
        raise



def setup_api_endpoints(app: Flask) -> None:
    """
    Set up API endpoints by registering the blueprint.
    """
    try:
        logger.info("Setting up API endpoints")
        from api.routes import endpoints_bp
        app.register_blueprint(endpoints_bp)
        logger.info("API endpoints registered successfully")
    except ImportError as e:
        logger.error(f"Failed to import routes module: {e}")
        raise ImportError("Unable to import API routes. Please check if routes.py exists and is properly configured.") from e
    except Exception as e:
        logger.error(f"Failed to setup API endpoints: {e}")
        raise



def setup_ml_modelling(model: str) -> None:
    """
    Set up ML modelling with error handling.
    """
    try:
        logger.info(f"Setting up ML modelling with model: {model}")
        llm_modelling.init(model)
        logger.info("ML modelling setup completed successfully")
    except Exception as e:
        logger.error(f"Failed to setup ML modelling: {e}")
        raise




def create_app(model: str = "openai") -> Flask:
    """
    Create and configure the Flask application.
    """
    global client, db, grid_fs
    try:
        print("======================================================")
        print("======================================================")
        logger.info("Starting Flask application creation")
        # Validate parameters
        validated_model = validate_model_parameter(model)
        logger.info(f"Validated parameters - model: {validated_model}")
        # Connect to MongoDB
        client, db = connect_to_mongodb(DEFAULT_URI, DEFAULT_DATABASE)
        # Set up GridFS
        grid_fs = setup_gridfs(db)
        # Create Flask app
        app = setup_flask_app()
        # Load environment variables
        load_environment_variables()
        # Set up API endpoints
        setup_api_endpoints(app)
        # Set up ML modelling
        setup_ml_modelling(validated_model)
        logger.info("Flask application created successfully")
        print("======================================================")
        return app
    
    except (ValueError, ConnectionFailure, ImportError) as e:
        # Re-raise specific exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during Flask application creation: {e}")
        raise Exception(f"Failed to create Flask application: {str(e)}") from e
    finally:
        # Cleanup on failure
        if 'app' not in locals() and client:
            logger.warning("Cleaning up MongoDB connection due to setup failure")
            try:
                client.close()
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup MongoDB connection: {cleanup_error}")


UPLOAD_FOLDER = DEFAULT_UPLOAD_FOLDER


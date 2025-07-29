#!/usr/bin/env python3
"""
Tests for Collections Transformer Flask server
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from api import create_app, connect_to_mongodb, setup_gridfs
from api.models import User, Dataset, Item


class TestServerBasic(unittest.TestCase):
    """Test basic server functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_model = "openai"
        self.test_port = 8081  # Use different port for testing
        
    def test_app_creation(self):
        """Test that Flask app can be created"""
        try:
            app = create_app(self.test_model)
            self.assertIsNotNone(app)
            self.assertEqual(app.name, 'api')
            print("Flask app creation test passed")
        except Exception as e:
            self.fail(f"App creation failed: {e}")
    
    def test_model_validation(self):
        """Test model parameter validation"""
        from api import validate_model_parameter
        
        # Test valid models
        valid_models = ["openai", "azure", "huggingface"]
        for model in valid_models:
            result = validate_model_parameter(model)
            self.assertEqual(result, model)
        
        # Test invalid model
        with self.assertRaises(ValueError):
            validate_model_parameter("invalid_model")
        
        print("Model validation test passed")


class TestMongoDBConnection(unittest.TestCase):
    """Test MongoDB connection functionality"""
    
    def test_mongodb_connection(self):
        """Test MongoDB connection setup"""
        try:
            client, db = connect_to_mongodb()
            self.assertIsNotNone(client)
            self.assertIsNotNone(db)
            
            # Test basic database operations
            test_collection = db['test_collection']
            test_doc = {"test": "data", "timestamp": "2024-01-01"}
            result = test_collection.insert_one(test_doc)
            self.assertIsNotNone(result.inserted_id)
            
            # Clean up
            test_collection.delete_one({"_id": result.inserted_id})
            client.close()
            
            print("MongoDB connection test passed")
        except Exception as e:
            self.fail(f"MongoDB connection failed: {e}")
    
    def test_gridfs_setup(self):
        """Test GridFS setup"""
        try:
            client, db = connect_to_mongodb()
            grid_fs = setup_gridfs(db)
            self.assertIsNotNone(grid_fs)
            client.close()
            print("GridFS setup test passed")
        except Exception as e:
            self.fail(f"GridFS setup failed: {e}")


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoints functionality"""
    
    def setUp(self):
        """Set up test Flask app"""
        self.app = create_app("openai")
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_health_check(self):
        """Test if server responds to basic requests"""
        try:
            # Test root endpoint (if exists)
            response = self.client.get('/')
            self.assertIn(response.status_code, [200, 404, 405])
            print("Health check test passed")
        except Exception as e:
            self.fail(f"Health check failed: {e}")
    
    def test_api_structure(self):
        """Test that API blueprint is registered"""
        try:
            # Check if API blueprint is registered
            registered_blueprints = list(self.app.blueprints.keys())
            self.assertIn('endpoints', registered_blueprints)
            print("API structure test passed")
        except Exception as e:
            self.fail(f"API structure test failed: {e}")


class TestModels(unittest.TestCase):
    """Test data models functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_user_id = "test_user_123"
        self.test_dataset_name = "test_dataset"
    
    @patch('api.models.user_collection')
    def test_user_creation(self, mock_user_collection):
        """Test user record creation"""
        try:
            # Mock the database operations
            mock_user_collection.find_one.return_value = None
            mock_user_collection.insert_one.return_value = MagicMock(inserted_id="test_id")
            mock_user_collection.update_one.return_value = MagicMock()
            
            # Test user connection recording
            User.record_connection(self.test_user_id, "login")
            
            # Verify the method was called
            mock_user_collection.insert_one.assert_called_once()
            print("User creation test passed")
        except Exception as e:
            self.fail(f"User creation test failed: {e}")
    
    @patch('api.models.dataset_collection')
    def test_dataset_operations(self, mock_dataset_collection):
        """Test dataset operations"""
        try:
            # Mock database operations
            mock_dataset_collection.find.return_value = []
            mock_dataset_collection.insert_one.return_value = MagicMock(inserted_id="test_dataset_id")
            
            # Test dataset retrieval
            datasets = Dataset.get_all(self.test_user_id)
            self.assertIsInstance(datasets, list)
            print("Dataset operations test passed")
        except Exception as e:
            self.fail(f"Dataset operations test failed: {e}")




def run_server_test():
    """Run a quick server test"""
    print("Starting Collections Transformer Server Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestServerBasic,
        TestMongoDBConnection,
        TestAPIEndpoints,
        TestModels,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        return True
    else:
        return False


if __name__ == '__main__':
    success = run_server_test()
    sys.exit(0 if success else 1)


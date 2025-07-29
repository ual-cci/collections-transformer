#!/usr/bin/env python3
"""
Main test runner for Collections Transformer
"""

import sys
import os
import time


def run_server_tests():
    """Run server tests"""
    print("\n" + "="*60)
    print("RUNNING SERVER TESTS")
    print("="*60)
    
    try:
        from test_server import run_server_test
        return run_server_test()
    except Exception as e:
        print(f"Server tests failed to run: {e}")
        return False


def run_frontend_tests():
    """Run frontend tests"""
    print("\n" + "="*60)
    print("RUNNING FRONTEND TESTS")
    print("="*60)
    
    try:
        from test_frontend import run_frontend_test
        return run_frontend_test()
    except Exception as e:
        print(f"Frontend tests failed to run: {e}")
        return False


def check_environment():
    """Check if the environment is properly set up"""
    print("\n" + "="*60)
    print("CHECKING ENVIRONMENT")
    print("="*60)
    
    base_dir = os.path.dirname(__file__)
    server_dir = os.path.join(base_dir, '..', 'server')
    client_dir = os.path.join(base_dir, '..', 'client')
    
    checks = []
    
    # Check server directory
    if os.path.exists(server_dir):
        checks.append("Server directory exists")
    else:
        checks.append("Server directory missing")
    
    # Check client directory
    if os.path.exists(client_dir):
        checks.append("Client directory exists")
    else:
        checks.append("Client directory missing")
    
    # Check Python environment
    if os.path.exists(os.path.join(server_dir, 'venv')):
        checks.append("Python virtual environment exists")
    else:
        checks.append("Python virtual environment not found")
    
    # Check Node.js environment
    if os.path.exists(os.path.join(client_dir, 'node_modules')):
        checks.append("Node.js dependencies installed")
    else:
        checks.append("Node.js dependencies not found")
    
    # Check MongoDB
    try:
        import pymongo
        checks.append("PyMongo available")
    except ImportError:
        checks.append("PyMongo not available")
    
    # Check Flask
    try:
        import flask
        checks.append("Flask available")
    except ImportError:
        checks.append("Flask not available")
    
    # Print all checks
    for check in checks:
        print(check)
    
    # Check for negative messages that indicate problems
    negative_indicators = ["missing", "not found", "not available"]
    has_problems = any(indicator in check.lower() for check in checks for indicator in negative_indicators)
    return not has_problems


def run_quick_test():
    """Run a quick test to verify basic functionality"""
    print("\n" + "="*60)
    print("QUICK FUNCTIONALITY TEST")
    print("="*60)
    
    try:
        # Test server app creation
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))
        from api import create_app
        
        app = create_app("openai")
        print("Flask app creation successful")
        
        # Test client structure
        client_dir = os.path.join(os.path.dirname(__file__), '..', 'client')
        package_json = os.path.join(client_dir, 'package.json')
        
        if os.path.exists(package_json):
            print("Frontend package.json found")
        else:
            print("Frontend package.json missing")
        
        # Test MongoDB connection
        try:
            from api import connect_to_mongodb
            client, db = connect_to_mongodb()
            print("MongoDB connection successful")
            client.close()
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"Quick test failed: {e}")
        return False


def main():
    
    start_time = time.time()
    results = {}
    
    # Check environment first
    env_ok = check_environment()
    
    # Run quick test
    quick_ok = run_quick_test()
    results['quick_test'] = quick_ok
    
    # Run comprehensive tests
    if env_ok and quick_ok:
        # Server tests
        server_ok = run_server_tests()
        results['server_tests'] = server_ok
        
        # Frontend tests
        frontend_ok = run_frontend_tests()
        results['frontend_tests'] = frontend_ok
        
    else:
        print("\n Skipping comprehensive tests due to environment issues")
        results['server_tests'] = False
        results['frontend_tests'] = False
    
    # Calculate results
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"Total time: {duration:.2f} seconds")
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Tests failed: {total_tests - passed_tests}/{total_tests}")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "="*60)
    if passed_tests == total_tests:
        return True
    else:
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)



#!/usr/bin/env python3
"""
Tests for Collections Transformer Frontend (Next.js)
Tests the frontend build process and basic functionality
"""

import unittest
import sys
import os
import json


class TestFrontendBuild(unittest.TestCase):
    """Test frontend build functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.client_dir = os.path.join(os.path.dirname(__file__), '..', 'client')
        self.package_json_path = os.path.join(self.client_dir, 'package.json')
        
    def test_package_json_exists(self):
        """Test that package.json exists and is valid"""
        try:
            self.assertTrue(os.path.exists(self.package_json_path))
            
            with open(self.package_json_path, 'r') as f:
                package_data = json.load(f)
            
            # Check required fields
            self.assertIn('name', package_data)
            self.assertIn('version', package_data)
            self.assertIn('dependencies', package_data)
            self.assertIn('scripts', package_data)
            
            # Check that it's a Next.js project
            self.assertIn('next', package_data.get('devDependencies', {}))
            self.assertIn('react', package_data.get('dependencies', {}))
            
            print("✅ Package.json validation test passed")
        except Exception as e:
            self.fail(f"Package.json test failed: {e}")
    
    def test_next_builds_exist(self):
        """Test that Next.js build directories exist"""
        try:
            next_dir = os.path.join(self.client_dir, '.next')
            next_builds_dir = os.path.join(self.client_dir, '.next-builds')
            
            # Check if build directories exist
            self.assertTrue(os.path.exists(next_dir) or os.path.exists(next_builds_dir))
            
            if os.path.exists(next_builds_dir):
                # Check for specific build directories
                build_dirs = os.listdir(next_builds_dir)
                self.assertGreater(len(build_dirs), 0)
                
                # Check for expected build directories
                expected_builds = ['next-openai-dev', 'next-openai-prod', 'next-azure-prod']
                for expected in expected_builds:
                    if expected in build_dirs:
                        build_path = os.path.join(next_builds_dir, expected)
                        self.assertTrue(os.path.isdir(build_path))
            
            print("Next.js builds test passed")
        except Exception as e:
            self.fail(f"Next.js builds test failed: {e}")
    
    def test_environment_configs(self):
        """Test that environment configurations exist"""
        try:
            env_files = [
                '.env.local',
                '.env.openai-dev',
                '.env.openai-prod',
                '.env.azure-dev',
                '.env.azure-prod'
            ]
            
            existing_env_files = []
            for env_file in env_files:
                env_path = os.path.join(self.client_dir, env_file)
                if os.path.exists(env_path):
                    existing_env_files.append(env_file)
            
            # At least one environment file should exist
            self.assertGreater(len(existing_env_files), 0)
            print(f"Environment configs test passed - Found: {existing_env_files}")
        except Exception as e:
            self.fail(f"Environment configs test failed: {e}")


class TestFrontendStructure(unittest.TestCase):
    """Test frontend directory structure"""
    
    def setUp(self):
        """Set up test environment"""
        self.client_dir = os.path.join(os.path.dirname(__file__), '..', 'client')
        
    def test_src_structure(self):
        """Test that src directory has expected structure"""
        try:
            src_dir = os.path.join(self.client_dir, 'src')
            self.assertTrue(os.path.exists(src_dir))
            
            # Check for expected directories
            expected_dirs = ['pages', '_components', '_helpers', 'styles']
            for expected_dir in expected_dirs:
                dir_path = os.path.join(src_dir, expected_dir)
                self.assertTrue(os.path.exists(dir_path), f"Directory {expected_dir} not found")
            
            print("Src structure test passed")
        except Exception as e:
            self.fail(f"Src structure test failed: {e}")
    
    def test_pages_exist(self):
        """Test that main pages exist"""
        try:
            pages_dir = os.path.join(self.client_dir, 'src', 'pages')
            self.assertTrue(os.path.exists(pages_dir))
            
            # Check for main pages
            expected_pages = [
                'index.js',
                'analyser.js',
                'ecosystem.js',
                'findpatterns.js',
                'newmodel.js',
                'uploaddataset.js',
                'user.js',
                'viewdataset.js'
            ]
            
            existing_pages = []
            for page in expected_pages:
                page_path = os.path.join(pages_dir, page)
                if os.path.exists(page_path):
                    existing_pages.append(page)
            
            # At least some main pages should exist
            self.assertGreater(len(existing_pages), 0)
            print(f"Pages test passed - Found: {existing_pages}")
        except Exception as e:
            self.fail(f"Pages test failed: {e}")
    
    def test_components_exist(self):
        """Test that components directory exists"""
        try:
            components_dir = os.path.join(self.client_dir, 'src', '_components')
            self.assertTrue(os.path.exists(components_dir))
            
            # Check for some key components
            component_files = os.listdir(components_dir)
            self.assertGreater(len(component_files), 0)
            
            print("Components test passed")
        except Exception as e:
            self.fail(f"Components test failed: {e}")


class TestFrontendDependencies(unittest.TestCase):
    """Test frontend dependencies"""
    
    def setUp(self):
        """Set up test environment"""
        self.client_dir = os.path.join(os.path.dirname(__file__), '..', 'client')
        self.package_json_path = os.path.join(self.client_dir, 'package.json')
    
    def test_scripts_exist(self):
        """Test that npm scripts are defined"""
        try:
            with open(self.package_json_path, 'r') as f:
                package_data = json.load(f)
            
            scripts = package_data.get('scripts', {})
            
            # Check for basic scripts
            basic_scripts = ['dev', 'build', 'start']
            for script in basic_scripts:
                self.assertIn(script, scripts, f"Missing script: {script}")
            
            # Check for environment-specific scripts
            env_scripts = ['dev-openai', 'build-openai', 'start-openai']
            found_env_scripts = []
            for script in env_scripts:
                if script in scripts:
                    found_env_scripts.append(script)
            
            self.assertGreater(len(found_env_scripts), 0)
            print(f"Scripts test passed - Found: {found_env_scripts}")
        except Exception as e:
            self.fail(f"Scripts test failed: {e}")




def run_frontend_test():
    """Run frontend tests"""
    print("Starting Collections Transformer Frontend Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestFrontendBuild,
        TestFrontendStructure,
        TestFrontendDependencies,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    if result.wasSuccessful():
        return True
    else:
        print(f"{len(result.failures)} tests failed, {len(result.errors)} tests had errors")
        return False


if __name__ == '__main__':
    success = run_frontend_test()
    sys.exit(0 if success else 1)


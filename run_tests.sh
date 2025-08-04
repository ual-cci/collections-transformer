#!/bin/bash

echo "Starting Tests"
echo "=================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$SCRIPT_DIR/tests"

if [ ! -d "$TESTS_DIR" ]; then
    echo "Error: Tests directory not found at $TESTS_DIR"
    echo "Please ensure you're running this script from the project root directory."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again."
    exit 1
fi

if [ ! -d "$SCRIPT_DIR/server" ] || [ ! -d "$SCRIPT_DIR/client" ]; then
    echo "Error: This script must be run from the project root directory"
    echo "Expected to find 'server' and 'client' directories in current location."
    echo "Current directory: $SCRIPT_DIR"
    echo "Found directories: $(ls -d */ 2>/dev/null | tr '\n' ' ')"
    exit 1
fi

if [ -d "$SCRIPT_DIR/server/venv" ]; then
    echo "Activating Python virtual environment"
    source "$SCRIPT_DIR/server/venv/bin/activate"
    echo "Virtual environment activated"
else
    echo "Warning: Python virtual environment not found"
    echo "Consider creating one: cd server && python3 -m venv venv"
fi

echo "Checking Python dependencies"
python3 -c "import flask, pymongo" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: Some Python dependencies may be missing"
    echo "   Consider installing: pip install flask pymongo requests"
fi

echo "Checking MongoDB status"
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet mongod; then
        echo "MongoDB is running"
    else
        echo "Warning: MongoDB may not be running"
        echo "Start with: sudo systemctl start mongod"
    fi
else
    echo "Warning: Cannot check MongoDB status (systemctl not available)"
fi

cd "$TESTS_DIR"
python3 run_all_tests.py

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed! Your application is ready to run."
else
    echo "Some tests failed. Please check the output above for details."
fi

exit $TEST_EXIT_CODE 


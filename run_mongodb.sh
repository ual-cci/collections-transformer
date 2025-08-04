#!/bin/bash

echo "Starting MongoDB"
echo "=================================================="
STATUS=$(systemctl is-active mongod)

if [ "$STATUS" = "active" ]; then
    echo "MongoDB is already running."
else
    echo "MongoDB is not running. Attempting to start it..."
    # Try to start without sudo
    systemctl start mongod
    # Re-check status
    STATUS=$(systemctl is-active mongod)
    if [ "$STATUS" = "active" ]; then
        echo "MongoDB started successfully."
    else
        echo "Failed to start MongoDB. Trying with sudo"
        sudo systemctl start mongod
        STATUS=$(systemctl is-active mongod)
        if [ "$STATUS" = "active" ]; then
            echo "MongoDB started successfully (with sudo)."
        else
            echo "Failed to start MongoDB."
            exit 1
        fi
    fi
fi

echo "Launching mongosh..."
mongosh

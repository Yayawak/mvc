#!/bin/bash

# CS Camp Crowdfunding System Run Script

echo "Starting CS Camp Crowdfunding System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate


# Run the application
echo "Starting application..."
echo "Using system Python with Tkinter support..."
/opt/homebrew/bin/python3 app.py

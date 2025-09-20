#!/bin/bash

# CS Camp Crowdfunding System Setup

echo "Setting up CS Camp Crowdfunding System..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Note: Tkinter requires system Python with Tk support
# If Tkinter doesn't work in virtual environment, use system Python:
# /opt/homebrew/bin/python3 app.py


echo "Setup complete! To run the application:"
echo "1. source venv/bin/activate"
echo "2. python app_csv.py"
echo ""
echo "Data is stored in CSV files in the 'data' directory."

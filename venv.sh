#!/bin/bash

# Create a virtual environment in the "venv" directory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
fi

# Confirm environment setup
echo "Virtual environment set up and dependencies installed!"
echo "To activate the virtual environment, run: source venv/bin/activate"

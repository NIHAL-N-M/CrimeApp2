#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Fix camera permissions for macOS
export OPENCV_AVFOUNDATION_SKIP_AUTH=1

# Start Django server
python manage.py runserver

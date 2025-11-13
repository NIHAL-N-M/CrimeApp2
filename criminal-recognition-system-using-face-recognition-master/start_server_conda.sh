#!/bin/bash

# Use conda base environment to run the app with compatible dlib/face_recognition
export OPENCV_AVFOUNDATION_SKIP_AUTH=1

# Run using conda-run to avoid inheriting any active virtualenv
exec conda run -n base python manage.py runserver

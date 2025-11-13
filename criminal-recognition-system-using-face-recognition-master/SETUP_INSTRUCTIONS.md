# Criminal Recognition System - Setup Complete! 🎉

## What's Been Done

✅ Installed all dependencies (Django, face_recognition, dlib, opencv)  
✅ Fixed code deprecation issues (textsize method)  
✅ Added error handling for image processing  
✅ Set up database with migrations  
✅ Created admin user for login  
✅ Configured camera permissions for macOS  

## How to Start the Application

### Start Command (Use This)
```bash
cd /Users/nihalmagnur/Desktop/criminal-recognition-system-using-face-recognition-master
export OPENCV_AVFOUNDATION_SKIP_AUTH=1
conda run -n base --no-capture-output python manage.py runserver
```

### Or use the script:
```bash
cd /Users/nihalmagnur/Desktop/criminal-recognition-system-using-face-recognition-master
./start_server_conda.sh
```

## Access the Application

Open your browser and go to: **http://127.0.0.1:8000/**

## Login Credentials

- **Email**: gayatri@gmail.com
- **Password**: gayatri

## Features Available

1. **Add Criminals** - Register criminals with their photos and details
2. **View Criminals** - See all criminals in the database
3. **Detect from Image** - Upload a photo to identify criminals
4. **Detect from Webcam** - Use live camera to identify criminals (press 'q' to quit)
5. **Track Criminals** - View last spotted locations of wanted criminals

## Important Notes

### Camera Permissions (macOS)
When using webcam detection for the first time:
1. Go to **System Settings > Privacy & Security > Camera**
2. Grant camera access to **Terminal** or your Python installation
3. Restart the server after granting permissions

### Adding Criminals
Before you can detect anyone, you need to:
1. Go to "Add Criminals" section
2. Fill in the form with criminal details
3. Upload a clear photo of their face
4. Submit the form

The system will now be able to recognize this person in photos or via webcam.

### Webcam Detection
- Press 'q' to quit the webcam view
- The system will draw boxes around detected faces
- Recognized criminals will show their details

## Troubleshooting

### If camera doesn't work:
```bash
# Grant camera permissions in System Settings, then restart with:
export OPENCV_AVFOUNDATION_SKIP_AUTH=1
python manage.py runserver
```

### If you get import errors:
The dlib library is linked from conda. Make sure you're using the virtual environment:
```bash
source .venv/bin/activate
```

### To stop the server:
Press `Ctrl + C` in the terminal

## Technical Stack

- Python 3.12
- Django 3.2.3
- face_recognition 1.3.0
- dlib 19.24.2
- OpenCV 4.12.0
- SQLite database

Enjoy using your Criminal Recognition System! 🚀

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.conf import settings
import bcrypt
from PIL import Image, ImageDraw
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
# Lazy import serializers/models inside functions to avoid multiprocessing spawn issues on macOS
from django.contrib.auth import logout
import threading
import os


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    from .serializers import FileSerializer
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Simple login gate

def _require_login(request):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to continue')
        return False
    return True

# view for index
def index(request):
    return render(request, 'session/login.html')


#view for log in
def login(request):
    from .models import User
    if((User.objects.filter(email=request.POST['login_email']).exists())):
        user = User.objects.filter(email=request.POST['login_email'])[0]
        if ((request.POST['login_password']== user.password)):
            request.session['id'] = user.id
            request.session['name'] = user.first_name
            request.session['surname'] = user.last_name
            messages.add_message(request,messages.INFO,'Welcome to criminal detection system '+ user.first_name+' '+user.last_name)
            return redirect(success)
        else:
            messages.error(request, 'Oops, Wrong password, please try a diffrerent one')
            return redirect('/')
    else:
        messages.error(request, 'Oops, That police ID do not exist')
        return redirect('/')


#view for log out
def logOut(request):
    logout(request)
    messages.add_message(request,messages.INFO,"Successfully logged out")
    return redirect(index)


# view to add crimina
def addCitizen(request):
   if not _require_login(request):
       return redirect(index)
   return render(request, 'home/add_citizen.html')


# view to add save citizen
def saveCitizen(request):
    if not _require_login(request):
        return redirect(index)
    from .models import Criminal
    if request.method == 'POST':
        citizen=Criminal.objects.filter(aadhar_no=request.POST["aadhar_no"])
        if citizen.exists():
            messages.error(request,"Citizen with that Aadhar Number already exists")
            return redirect(addCitizen)
        else:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            # Store a clean relative filesystem path like "media/filename with spaces.jpg"
            rel_path = os.path.join(settings.MEDIA_URL.strip('/'), filename)

            criminal = Criminal.objects.create(
                name=request.POST["name"],
                aadhar_no=request.POST["aadhar_no"],
                address=request.POST["address"],
                picture=rel_path,
                status="Free"
            )
            criminal.save()
            messages.add_message(request, messages.INFO, "Citizen successfully added")
            return redirect(viewCitizens)


# view to get citizen(criminal) details
def viewCitizens(request):
    if not _require_login(request):
        return redirect(index)
    from .models import Criminal
    citizens=Criminal.objects.all();
    context={
        "citizens":citizens
    }
    return render(request,'home/view_citizens.html',context)


#view to set criminal status to wanted
def wantedCitizen(request, citizen_id):
    if not _require_login(request):
        return redirect(index)
    from .models import Criminal
    wanted = Criminal.objects.filter(pk=citizen_id).update(status='Wanted')
    if (wanted):
        messages.add_message(request,messages.INFO,"User successfully changed status to wanted")
    else:
        messages.error(request,"Failed to change the status of the citizen")
    return redirect(viewCitizens)

#view to set criminal status to free
def freeCitizen(request, citizen_id):
    if not _require_login(request):
        return redirect(index)
    from .models import Criminal
    free = Criminal.objects.filter(pk=citizen_id).update(status='Free')
    if (free):
        messages.add_message(request,messages.INFO,"User successfully changed status to Found and Free from Search")
    else:
        messages.error(request,"Failed to change the status of the citizen")
    return redirect(viewCitizens)


def spottedCriminals(request):
    if not _require_login(request):
        return redirect(index)
    from .models import CriminalLastSpotted
    thiefs=CriminalLastSpotted.objects.filter(status="Wanted")
    context={
        'thiefs':thiefs
    }
    return render(request,'home/spotted_thiefs.html',context)


def foundThief(request,thief_id):
    if not _require_login(request):
        return redirect(index)
    from .models import CriminalLastSpotted, Person
    free = CriminalLastSpotted.objects.filter(pk=thief_id)
    freectzn = CriminalLastSpotted.objects.filter(aadhar_no=free.get().aadhar_no).update(status='Found')
    if(freectzn):
        thief = CriminalLastSpotted.objects.filter(pk=thief_id)
        free = Person.objects.filter(aadhar_no=thief.get().aadhar_no).update(status='Found')
        if(free):
            messages.add_message(request,messages.INFO,"Thief updated to found, congratulations")
        else:
            messages.error(request,"Failed to update thief status")
    return redirect(spottedCriminals)


# Admin-only: clear all criminal data and media

def clearDatabase(request):
    if not _require_login(request):
        return redirect(index)
    from .models import User, Criminal, CriminalLastSpotted
    # Simple admin check by email
    try:
        user = User.objects.get(id=request.session['id'])
        is_admin = (user.email == 'jnnce@gmail.com')
    except Exception:
        is_admin = False
    if not is_admin:
        messages.error(request, 'Only admin can clear the database.')
        return redirect('/success')

    if request.method == 'POST':
        # Delete media files for criminals
        deleted_files = 0
        for c in Criminal.objects.all():
            try:
                p = _abs_media_path(c.picture)
                if os.path.isfile(p):
                    os.remove(p)
                    deleted_files += 1
            except Exception:
                pass
        Criminal.objects.all().delete()
        CriminalLastSpotted.objects.all().delete()
        # Also clean results dir
        try:
            results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
            if os.path.isdir(results_dir):
                for name in os.listdir(results_dir):
                    try:
                        os.remove(os.path.join(results_dir, name))
                    except Exception:
                        pass
        except Exception:
            pass
        messages.success(request, f"Database cleared. Removed {deleted_files} files and all records.")
        return redirect('/success')

    # GET -> show confirmation on dashboard via message
    messages.info(request, 'Submit the Clear Database form to confirm.')
    return redirect('/success')





def success(request):
    from .models import User
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'home/welcome.html', context)


# Utility to normalize stored/URL paths to absolute filesystem paths
from urllib.parse import unquote

def _abs_media_path(p):
    # Remove possible leading slash and percent-decode
    p = unquote(p or '')
    if p.startswith('/'):
        # allow absolute paths under BASE_DIR
        abs_try = p
    else:
        abs_try = os.path.join(settings.BASE_DIR, p)
    return abs_try

# view to detect and recognise faces
def detectImage(request):
    if not _require_login(request):
        return redirect(index)
    # function to detect faces and draw a rectangle around the faces
    # with correct face label

    # Lazy imports to avoid requiring heavy deps at server startup
    import face_recognition
    import numpy as np

    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

    # Build known face encodings from DB images
    known_face_encodings = []
    known_face_names = []

    from .models import Criminal
    prsn = Criminal.objects.all()
    import cv2
    for criminal in prsn:
        try:
            img_path = _abs_media_path(criminal.picture)
            img_bgr = cv2.imread(img_path)
            if img_bgr is None:
                # Fallback to PIL (handles some formats better)
                try:
                    from pillow_heif import register_heif_opener
                    try:
                        register_heif_opener()
                    except Exception:
                        pass
                    pil_img = Image.open(img_path).convert('RGB')
                    img_rgb = np.ascontiguousarray(np.array(pil_img), dtype=np.uint8)
                except Exception as e2:
                    print(f"Could not load image via OpenCV or PIL: {img_path}: {e2}")
                    continue
            else:
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)
            face_encs = face_recognition.face_encodings(img_rgb)
            if face_encs:
                known_face_encodings.append(face_encs[0])
                known_face_names.append(criminal.name + ' ' + criminal.address)
            else:
                print(f"No face detected in: {img_path}")
        except Exception as e:
            print(f"Error processing {criminal.picture}: {e}")
            continue




    # known_face_encodings and known_face_names already built above

    # loading the image that is coming from the front end
    import cv2, os
    img_path = uploaded_file_url[1:]
    img_path = _abs_media_path(img_path)
    unknown_img = cv2.imread(img_path)
    if unknown_img is None:
        # Try PIL fallback (for formats OpenCV can't read, e.g., HEIC)
        try:
            from pillow_heif import register_heif_opener
            try:
                register_heif_opener()
            except Exception:
                pass
            pil_img = Image.open(img_path).convert('RGB')
            unknown_image = np.ascontiguousarray(np.array(pil_img), dtype=np.uint8)
        except Exception:
            messages.error(request, "Could not load uploaded image. Please upload a JPG or PNG.")
            return redirect('/success')
    else:
        unknown_image = cv2.cvtColor(unknown_img, cv2.COLOR_BGR2RGB)

    # finding face locations and encoding of that image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # converting the image to PIL format
    pil_image = Image.fromarray(unknown_image)
    #Draw a rectangle over the face
    draw = ImageDraw.Draw(pil_image)

    # run a for loop to find if faces in the input image matches to that 
    # of our encoding present in the DB
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        
        # Only check for matches if we have known faces in DB
        if len(known_face_encodings) > 0:
            # compare the face to the criminals present
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # find distance w.r.t to the faces of criminals present in the DB
            # take the minimum distance
            # see if it matches the faces
            # if matches update the name variable to the respective criminal name
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]


        # with pollow module draw a rectangle around the face
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # put a label of name of the person below
        bbox = draw.textbbox((0, 0), name)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory 
    del draw

    # save annotated image to media/results
    results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    out_path = os.path.join(results_dir, f"{base_name}_annotated.jpg")
    try:
        pil_image.save(out_path, format='JPEG')
        rel_out = os.path.relpath(out_path, settings.BASE_DIR)
        messages.success(request, f"Processed image saved: /{rel_out}")
    except Exception as e:
        messages.error(request, f"Processed, but failed to save result: {e}")

    return redirect('/success')



# Use a separate process for webcam UI on macOS to avoid NSWindow main-thread crash
from multiprocessing import Process
WEBCAM_PROC = None


def _run_webcam_loop(known_face_encodings, known_face_names, n_id):
    # Ensure Django is set up in the child process
    try:
        import django
        django.setup()
    except Exception:
        pass
    import face_recognition
    import numpy as np
    import cv2

    try:
        # Access camera
        video_capture = cv2.VideoCapture(0)
        try:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            video_capture.set(cv2.CAP_PROP_FOURCC, fourcc)
            video_capture.set(cv2.CAP_PROP_FPS, 30)
        except Exception:
            pass
        try:
            video_capture.set(cv2.CAP_PROP_CONVERT_RGB, 1)
        except Exception:
            pass
        if not video_capture.isOpened():
            print("Cannot access camera. Grant permissions in System Settings > Privacy & Security > Camera.")
            return

        while True:
            ret, frame = video_capture.read()
            if not ret or frame is None:
                print("Failed to read frame from camera")
                break

            if len(frame.shape) == 2:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            elif frame.shape[2] == 4:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            else:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if rgb_frame.dtype != np.uint8:
                rgb_frame = cv2.convertScaleAbs(rgb_frame)
            rgb_frame = np.ascontiguousarray(rgb_frame, dtype=np.uint8)

            if rgb_frame.ndim != 3 or rgb_frame.shape[2] != 3 or rgb_frame.dtype != np.uint8:
                print(f"Invalid frame for face_recognition: shape={rgb_frame.shape}, dtype={rgb_frame.dtype}")
                continue

            try:
                face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            except RuntimeError as e:
                print(f"face_locations RuntimeError: {e}; retrying with grayscale")
                try:
                    gray = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2GRAY)
                    gray = np.ascontiguousarray(gray, dtype=np.uint8)
                    face_locations = face_recognition.face_locations(gray, model="hog")
                except RuntimeError as e2:
                    print(f"grayscale fallback failed: {e2}; skipping frame")
                    continue
            try:
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            except RuntimeError as e:
                print(f"face_encodings RuntimeError: {e}; skipping frame")
                continue

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Unknown"
                if len(known_face_encodings) > 0:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances) if len(face_distances) else None
                    if best_match_index is not None and matches[best_match_index]:
                        ntnl_id = n_id[best_match_index]
                        from .models import Criminal, CriminalLastSpotted
                        criminal = Criminal.objects.filter(aadhar_no=ntnl_id)
                        name = known_face_names[best_match_index] + ', Status: ' + criminal.get().status
                        if criminal.get().status == 'Wanted':
                            thief = CriminalLastSpotted.objects.create(
                                name=criminal.get().name,
                                aadhar_no=criminal.get().aadhar_no,
                                address=criminal.get().address,
                                picture=criminal.get().picture,
                                status='Wanted',
                                latitude='25.3176° N',
                                longitude='82.9739° E'
                            )
                            thief.save()

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        try:
            video_capture.release()
        except Exception:
            pass
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass


# View to detect criminals using webcam

def detectWithWebcam(request):
    if not _require_login(request):
        return redirect(index)
    import face_recognition
    import numpy as np
    import cv2
    import os

    # Build known encodings and names/ids from DB (outside thread)
    known_face_encodings = []
    known_face_names = []
    n_id = []

    from .models import Criminal
    prsn = Criminal.objects.all()
    for criminal in prsn:
        try:
            img_path = criminal.picture
            if not os.path.isabs(img_path):
                img_path = os.path.join(settings.BASE_DIR, img_path)
            img_bgr = cv2.imread(img_path)
            if img_bgr is None:
                print(f"Could not load image: {img_path}")
                continue
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)
            face_encs = face_recognition.face_encodings(img_rgb)
            if face_encs:
                known_face_encodings.append(face_encs[0])
                known_face_names.append('Name: ' + criminal.name + ', AadharNo: ' + criminal.aadhar_no + ', Address ' + criminal.address)
                n_id.append(criminal.aadhar_no)
        except Exception as e:
            print(f"Error processing {criminal.picture}: {e}")
            continue

    # Launch webcam in a separate process so OpenCV HighGUI runs on a main thread
    global WEBCAM_PROC
    if WEBCAM_PROC is not None and WEBCAM_PROC.is_alive():
        messages.info(request, "Webcam is already running. Switch to the 'Video' window or press q to quit it.")
        return redirect('/success')

    proc = Process(target=_run_webcam_loop, args=(known_face_encodings, known_face_names, n_id), daemon=True)
    proc.start()
    WEBCAM_PROC = proc
    messages.success(request, "Webcam started. A window named 'Video' should appear. Press q to exit.")
    return redirect('/success')




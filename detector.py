import cv2 as cv
import json
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import threading
from playsound import playsound
from ultralytics.nn.tasks import DetectionModel



camera = cv.VideoCapture(0)
model = YOLO("bestface.pt")
weapon_model = YOLO("best_me.pt")
# weapon_model = YOLO("best_lastTry.pt")

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainneruser.yml')

#open users json file and retrieve names
with open('users.json') as jsonFile:
    users = json.load(jsonFile)
userList = []



def detector():
    """
    Run live face detection and user recognition on the default webcam.

    Behavior:
    - Reads frames from `camera` and detects faces with the YOLO face model.
    - Predicts user ID using the LBPH recognizer (`trainneruser.yml`).
    - Overlays bounding boxes and recognized names (or 'Unknown') on the frame.
    - Displays a window titled 'Image' until 'q' is pressed.

    Side effects:
    - Opens and reads the default webcam.
    - Renders a live window; press 'q' to exit and release the camera.
    """
    # Capture video on webcam
    count = 0

    #loop over the frames
    while 1:
        #read frames
        ret, image = camera.read()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        height, width = image.shape[:2]
        result = model.predict(image)
        for r in result:
            annotator = Annotator(image)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                cv.rectangle(image, (x,y), (w, h), (100,0,100), 2)
                faceId, mismatch = recognizer.predict(gray[y:y+h, x:x+w])
                faceId=str(faceId)
                if mismatch < 50  :
                    if faceId in users :
                        userList.append(faceId)
                        faceId = users[str(faceId)]['name'] + " " + users[str(faceId)]['mode']
                    else:
                        faceId = 'Unknown'
                else:
                    faceId = 'Unknown'
                cv.putText(image, str(faceId), (x,y),cv.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

        cv.imshow('Image',image)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()


def detectorcrim():
    """
    Run live face detection and criminal identification with audible alert.

    Behavior:
    - Loads LBPH recognizer data from `trainnercrim.yml` and criminal metadata
      from `criminals.json`.
    - Detects faces via the YOLO face model and predicts IDs via LBPH.
    - If a recognized criminal is detected (low mismatch), overlays the name
      and plays `alarm3.wav` in a background thread.
    - Displays a window titled 'Image' until 'q' is pressed.

    Side effects:
    - Accesses webcam, reads JSON, and plays sound from `alarm3.wav`.
    - Shows a live preview window; press 'q' to exit and release resources.
    """
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read('trainnercrim.yml')

    with open('criminals.json') as jsonFile2:
        crims = json.load(jsonFile2)
        crimList = []
    # Capture video on webcam
    count = 0

    #loop over the frames
    while 1:
        #read frames
        ret, image = camera.read()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        height, width = image.shape[:2]
        result = model.predict(image)
        for r in result:
            annotator = Annotator(image)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                cv.rectangle(image, (x,y), (w, h), (100,0,100), 2)

                faceId, mismatch = recognizer.predict(gray[y:y+h, x:x+w])
                faceId=str(faceId)
                if mismatch < 50  :
                    if faceId in crims :
                        crimList.append(faceId)
                        faceId = crims[str(faceId)]['name']
                        alarm_thread = threading.Thread(target=playsound, args=("alarm3.wav",))
                        alarm_thread.start()
                    else:
                        faceId = 'Unknown'
                else:
                    faceId = 'Unknown'
                cv.putText(image, str(faceId), (x,y),cv.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)
                

        cv.imshow('Image',image)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()


def live_detection():
    """
    Perform simultaneous weapon detection and face recognition from the webcam.

    Behavior:
    - Detects weapons(Guns/knifes) using `weapon_model` and labels them on the frame.
    - Detects faces using the YOLO face model and recognizes users via LBPH
      (`trainneruser.yml`, loaded globally).
    - Overlays labels for weapons and recognized user names (or 'Unknown').
    - Displays a window titled 'Image' until 'q' is pressed.

    Side effects:
    - Opens a new VideoCapture and a display window; press 'q' to exit.
    - Utilizes global models `model`, `weapon_model`, and `recognizer`.
    """

    camera = cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            # detect weapon
            result = weapon_model.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, weapon_model.names[int(c)], 3)
            #detect face
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            height, width = frame.shape[:2]
            result = model.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                    cv.rectangle(frame, (x,y), (w, h), (100,0,100), 2)
                    faceId, mismatch = recognizer.predict(gray[y:y+h, x:x+w])
                    faceId=str(faceId)
                    if mismatch < 50  :
                        if faceId in users :
                            userList.append(faceId)
                            faceId = users[str(faceId)]['name'] + " " + users[str(faceId)]['mode']
                        else:
                            faceId = 'Unknown'
                    else:
                        faceId = 'Unknown'
                    cv.putText(frame, str(faceId), (x,y),cv.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

        cv.imshow('Image', frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()

# detector()
# detectorcrim()
# live_detection()



import cv2 as cv
import json
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
import threading
from playsound import playsound

camera = cv.VideoCapture(0)
model = YOLO("bestface.pt")
model2 = YOLO("best_me.pt")
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainneruser.yml')

#open users json file and retrieve names
with open('users.json') as jsonFile:
    users = json.load(jsonFile)
userList = []



def detector():
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

    camera = cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            # detect weapon
            result = model2.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, model2.names[int(c)], 3)
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



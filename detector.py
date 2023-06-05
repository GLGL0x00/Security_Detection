import cv2 as cv
import json
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator

model = YOLO("bestface.pt")
model2 = YOLO("weapondetection.pt")
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainner.yml')

#open users json file and retrieve names
with open('users.json') as jsonFile:
    users = json.load(jsonFile)
userList = []
def detector():
    camera = cv.VideoCapture(0)
    # Capture video on webcam
    count = 0

    #Detect face and recognize 

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
                # annotator.box_label(b, model.names[int(c)], 3)
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                cv.rectangle(image, (x, y), (x + w, y + h), (100, 100, 0), 2)
                # cv.rectangle(image, (x,y), (w, h), (100,0,100), 2)

                faceId, percentage = recognizer.predict(gray[y:y+h, x:x+w])
                print(faceId, percentage)
                faceId=str(faceId)
                if percentage < 50 :
                    userList.append(faceId)
                    faceId = users[str(faceId)]['name']
                else:
                    faceId = 'Unknown'

                cv.putText(image, faceId, (x,y),cv.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

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
                    annotator.box_label(b, model.names[int(c)], 3)
                    x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                    # cv.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 0), 2)
                    # cv.rectangle(frame, (x,y), (w, h), (100,0,100), 2)

                    faceId, percentage = recognizer.predict(gray[y:y + h, x:x + w])
                    print(faceId, percentage)
                    faceId = str(faceId)
                    if percentage < 50:
                        userList.append(faceId)
                        faceId = users[str(faceId)]['name']
                    else:
                        faceId = 'Unknown'

                    cv.putText(frame, faceId, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (50, 255,), 2)

        cv.imshow('Image', frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()
# detector()
# live_detection()



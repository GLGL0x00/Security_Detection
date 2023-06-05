from flask import Flask,render_template,Response,redirect,request
import cv2 as cv
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
import threading
from send_emails import send_emails
from playsound import playsound
import pyrebase
import random
import datetime
import json

# run app and model and open camera
app = Flask(__name__)
model = YOLO("weapondetection.pt")
model2 = YOLO("bestface.pt")
# load recognizer and users
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainner.yml')

# open users json file and retrieve names
with open('users.json') as jsonFile:
    users = json.load(jsonFile)

# handle DataBase
firebaseConfig = {
    "apiKey": "AIzaSyAnhloXy_qVpeLDydEkAQ878aYPoSuW1q4",
    "authDomain": "competition-a5c93.firebaseapp.com",
    "databaseURL": "https://competition-a5c93-default-rtdb.firebaseio.com/",
    "projectId": "competition-a5c93",
    "storageBucket": "competition-a5c93.appspot.com",
    "messagingSenderId": "72680403206",
    "appId": "1:72680403206:web:1262babdacad10df71ae87",
    "measurementId": "G-CNL7R6TF4L",
    "serviceAccount": "comptation.json"
}

firebase=pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()
database=firebase.database()
auth = firebase.auth()

def faceRecognation(frame):

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = frame.shape[:2]
    userList = []
    result = model2.predict(frame)
    for r in result:
        annotator = Annotator(frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            c = box.cls
            x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
            annotator.box_label(b, model2.names[int(c)], 3)
            # cv.rectangle(frame, (x, y), (w, h), (100, 0, 100), 2)
            faceId, percentage = recognizer.predict(gray[y:y + h, x:x + w])
            faceId = str(faceId)
            if percentage < 50:
                userList.append(faceId)
                faceId = users[str(faceId)]['name']
            else:
                faceId = 'Unknown'

            cv.putText(frame, faceId, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (50, 255,), 2)

def tracking(frame,x, y, w, h):
    tracker = cv.TrackerCSRT_create()
    tracker.init(frame, [x, y, w, h])
    success, bbox = tracker.update(frame)
    # Draw the bounding box around the tracked object
    if success:
        x, y, w, h = [int(i) for i in bbox]
        cv.rectangle(frame, (x-50, y-50), (x + w+50, y + h+50), (0, 255, 0), 3)


def uploadphoto():
    data={
        'name':"unkown",
        'date':str(datetime.datetime.now())
    }
    Id = random.randrange(1, 9999, 5)
    database.child("udjat").child("unknown"+str(Id)).update(data)
    storage.child("udjat").child("unknown"+str(Id)+".jpg").put("screenShot3.jpg")
def screenshoot(frame):
    count=0
    if count % 10 == 0:
        cv.imwrite(f'screenshot_4.jpg', frame)
    count += 1

camera = cv.VideoCapture(0)
def generate_frames():
    camera = cv.VideoCapture(0)

    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            result = model.predict(frame ,classes=[0,1])
            for r in result:
                annotator = Annotator(frame)
                facethread=threading.Thread(target=faceRecognation(frame))
                boxes=r.boxes
                for box in boxes:
                    b=box.xyxy[0]
                    c=box.cls
                    # annotator.box_label(b,model.names[int(c)],3)
                    # print( int(b[0]),int(c) ) #return class name , c class id
                    x, y, w, h= int(b[0]),int(b[1]),int(b[2]),int(b[3])
                    detectcoun=1
                    if int(c)==1 or int(c)==0:
                        # screenshootthread=threading.Thread(target=screenshoot(frame))
                        x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                        annotator.box_label(b, model.names[int(c)], 3)
                        # cv.rectangle(frame, (x,y), (x + w, y + h), (0, 0, 255), 2)
                        # TrackingThread = threading.Thread(target=tracking(frame,x, y, w, h))
                        # AlarmThread = threading.Thread(target=playsound, args=("alarm3.wav",))
                        cv.imwrite("screenShot3.jpg", frame)
                        # UploadPhotoThread=threading.Thread(target=uploadphoto())
                        # MailThread =threading.Thread(target=send_emails())

                    # screenshootthread.start()
                    # TrackingThread.start()
                    # AlarmThread.start()
                    # UploadPhotoThread.start()
                    # MailThread.start()
                    detectcoun+=1
                facethread.start()

                    # frame=annotator.result()
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def GenerateFrame():
#     camera=cv.VideoCapture(0)
#     while True:
#         res,frame=camera.read()
#         if not res:
#             break
#         else:
#             ret,buffer=cv.imencode('.jpg',frame)
#             frame=buffer.tobytes()
#         yield(b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/' )
def login():
    return render_template('login.html',custom_css='static\css\login.css',title=" login ",icon="static\img\icon.png")

@app.route('/' , methods=['POST'])
def checklog():
    email=request.form["email"]
    password=request.form["password"]
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return redirect("/home")
    except:
        return render_template('login.html', message='Login failed' , custom_css='static\css\login.css')


@app.route("/home")
def homepage():
    return render_template('home.html',custom_css='static\css\cameras.css', htitle="Home",icon="static\img\icon.png")

@app.route('/home' , methods=['POST'])
def close():
    camera.release()
    return redirect('/')

@app.route("/detections")
def detections():
    all_files=storage.child("udjat").list_files()
    imgs = [file for file in all_files if file.name.endswith('.jpg') or file.name.endswith('.png')]
    links = [storage.child(file.name).get_url(None) for file in imgs]
    # images = storage.child("udjat").list_files()
    # image_urls = []
    # for image in images:
    #     image_url = storage.child(image.name).get_url(None)
    #     image_urls.append(image_url)

    return render_template('detections2.html',images=links ,custom_css='static\css\detections2.css', title=" Detection",icon="static\img\icon.png")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)
import cv2 as cv
import os
from PIL import Image
import numpy as np
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator

def trainner():
    faceArr, ids = [], []

    recognizer = cv.face.LBPHFaceRecognizer.create()

    # cascade = cv.CascadeClassifier('.\Face_recognize\haarcascade_frontalface_default.xml')
    model = YOLO("bestface.pt")

    imagePath = [os.path.join('dataset',f) for f in os.listdir('dataset')]
    # print(imagePath)

    for paths in imagePath:
        # if os.path.split(paths)[-1].split('.')[-1] != 'jpg':
        #     continue

        img = Image.open(paths).convert('L')

        imgArr = np.array(img,'uint8')
    
        faceId = int(os.path.split(paths)[-1].split('.')[1])

        result = model.predict(img)
        for r in result:
            annotator = Annotator(imgArr)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                faceArr.append(imgArr[y:y+h, x:x+w])
                ids.append(faceId)

    recognizer.train(faceArr,np.array(ids))
    recognizer.save('trainneruser.yml')

# trainner()
def trainnerwithpath(path):
    faceArr, ids = [], []

    recognizer = cv.face.LBPHFaceRecognizer.create()

    model = YOLO("bestface.pt")

    imagePath = [os.path.join(path,f) for f in os.listdir(path)]
    # print(imagePath)

    for paths in imagePath:
        # if os.path.split(paths)[-1].split('.')[-1] != 'jpg':
        #     continue

        img = Image.open(paths).convert('L')
        imgArr = np.array(img,'uint8')

        faceId = int(os.path.split(paths)[-1].split('.')[1])

        result = model.predict(img)
        for r in result:
            annotator = Annotator(imgArr)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                faceArr.append(imgArr[y:y+h, x:x+w])
                ids.append(faceId)

    recognizer.train(faceArr,np.array(ids))
    recognizer.save('trainnercrim.yml')
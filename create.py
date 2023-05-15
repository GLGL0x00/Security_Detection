from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
import cv2 as cv
import os,pickle
import face_recognition
from random import randint

#save images
def takephoto():
    Id=randint(0,100)
    name=input("enter your name : ")
    while name.isdigit():
        print('enter only alpha')
        name = input('Enter Name : ')
    model=YOLO("facedetect.pt")
    # img="imgs/all.jpg"
    # res=model.predict(source=img , show=True,save_crop=True)

    camera = cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            result=model.predict(frame,show=True, save_crop=True)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    if cv.waitKey(32) & 0xFF == ord('s'):
                        print("done")
                        cv.imwrite('imgs/ '+name+'.jpg', frame[int(box.xyxy[0][1]):int(box.xyxy[0][3]),int(box.xyxy[0][0]):int(box.xyxy[0][2])])

# takephoto()

# load images
folderpath="imgs"
pathlist=os.listdir(folderpath)
print(pathlist)
imglist=[]
employeenameslist=[]
for path in pathlist:
    imglist.append(cv.imread(os.path.join(folderpath,path)))
    employeenameslist.append(os.path.splitext(path)[0])

print(employeenameslist)

def encodingImgs(imageslist):
    encodedList=[]
    for img in imageslist:
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodedList.append(encode)
    return encodedList

encodeKnown=encodingImgs(imglist)
encodeKnownWithNames= [encodeKnown,employeenameslist]
print(encodeKnownWithNames)

file=open("EncodedImgs.p",'wb')
pickle.dump(encodeKnownWithNames,file)
file.close()
print("file saved")




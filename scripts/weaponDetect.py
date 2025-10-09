import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
# model = YOLO("E:\\Mine\\Security detection\\train attempts\\yolov8n_wlr2-Last try\\yolov8n_wlr2\\weights\\best.pt")
model = YOLO("E:\\Ahmed\\Security detection\\train attempts\\yolov8n_wlr2-Last try\\weights\\best.pt")

def weapondetecter():

    camera = cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            result = model.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)], 3)
        cv.imshow('Image', frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()

# weapondetecter()
import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
import os
from trainner import  trainnerwithpath
from random import randint
import json

# Load the YOLO object detection models
model = YOLO('best_me.pt')  # Load the first model
model2 = YOLO('yolov8n.pt')  # Load the second model

# Create a Mediapipe hand object
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

# Create a VideoCapture object to read frames from the webcam
cap = cv2.VideoCapture(0)

def tracker():
    # Initialize variables for object and hand tracking
    object_bbox = None
    object_tracking = False
    hand_bbox = None
    id = randint(100, 150)
    counter = 0
    #Create a directory to save the screenshots
    screenshot_dir = 'screenshots'
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        # Convert the frame to RGB for Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe hand pose estimation
        results_hands = mp_hands.process(frame_rgb)

        # Process the frame with YOLO object detection (model)
        result = model(frame)

        # Process the frame with YOLO object detection (model2)
        result2 = model2(frame, classes=[0],max_det=1)


        # Check if hands were detected
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                # Convert hand landmarks to integer points
                hand_points = [
                    (int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks.landmark
                ]

                # Get the bounding box coordinates of the hand
                hand_bbox = cv2.boundingRect(np.array(hand_points))

                # Draw hand landmarks on the frame
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )

        # Draw bounding boxes on the frame for model1
        annotator = Annotator(frame)
        for r in result:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                annotator.box_label(b, model.names[int(c)], 3)
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])

                # Check if the bounding box of model1 intersects with the hand bounding box
                if hand_bbox is not None and (
                        x < hand_bbox[0] + hand_bbox[2] and x + w > hand_bbox[0] and
                        y < hand_bbox[1] + hand_bbox[3] and y + h > hand_bbox[1]
                ):
                    # Draw bounding boxes on the frame for model2
                    for r2 in result2:
                        boxes2 = r2.boxes
                        for box2 in boxes2:
                            b2 = box2.xyxy[0]
                            c2 = box2.cls
                            annotator.box_label(b2, "criminal", 3)

                            # Check if the object bounding box of model2 intersects with the bounding box of model1
                            if (
                                    x < b2[0] + b2[2] and x + w > b2[0] and
                                    y < b2[1] + b2[3] and y + h > b2[1]
                            ):
                                # Crop the frame to the bounding box of model2
                                object_frame = frame[int(b2[1]):int(b2[3]), int(b2[0]):int(b2[2])]

                                # Save a screenshot of the object frame
                                screenshot_path = os.path.join(
                                    screenshot_dir, 'criminal.'+str(id)+'.'+str(counter)+'.jpg'
                                )
                                object_frame_gray = cv2.cvtColor(object_frame, cv2.COLOR_BGR2GRAY)
                                cv2.imwrite(screenshot_path, object_frame_gray)
                            counter+=1
                            if counter == 5:
                                break



        # Display the frame
        cv2.imshow('Object Tracking and Hand Pose Estimation', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the VideoCapture object and close the windows
    cap.release()
    cv2.destroyAllWindows()
    with open("criminals.json") as json_file2:
        data = json.load(json_file2)


    name = 'criminal'+ str(id)
    username = {
                'name':name
            }
    data[id] = username

    with open("criminals.json", "w") as file:
        json.dump(data, file,indent = 4)

    trainnerwithpath(screenshot_dir)

# tracker()
import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator

# Load the YOLO object detection model
model = YOLO('best_me.pt')  # load an official model

# Create a Mediapipe hand object
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Create a Mediapipe face detection object
mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)

# Create a VideoCapture object to read frames from the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for object and hand tracking
object_bbox = None
object_tracking = False
hand_bbox = None

# Initialize variables for face tracking
face_detected = False
face_tracker = cv2.TrackerKCF_create()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with YOLO object detection
    result = model(frame)

    # Draw bounding boxes on the frame
    annotator = Annotator(frame)
    for r in result:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            c = box.cls
            annotator.box_label(b, model.names[int(c)], 3)
            x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])

            # Check if the object bounding box intersects with the hand bounding box
            if object_tracking and hand_bbox is not None:
                if (x < hand_bbox[0] + hand_bbox[2] and x + w > hand_bbox[0] and
                        y < hand_bbox[1] + hand_bbox[3] and y + h > hand_bbox[1]):
                    # Expand the bounding box to contain the face
                    x = min(x, hand_bbox[0])
                    y = min(y, hand_bbox[1])
                    w = max(x + w, hand_bbox[0] + hand_bbox[2]) - x
                    h = max(y + h, hand_bbox[1] + hand_bbox[3]) - y
                    if frame.shape[0] > 0 and frame.shape[1] > 0:
                        # Process the frame with Mediapipe face detection
                        results_face = mp_face_detection.process(frame_rgb)
                        if results_face.detections:
                            for detection in results_face.detections:
                                bbox = detection.location_data.relative_bounding_box
                                bbox_x = int(bbox.xmin * frame.shape[1])
                                bbox_y = int(bbox.ymin * frame.shape[0])
                                bbox_w = int(bbox.width * frame.shape[1])
                                bbox_h = int(bbox.height * frame.shape[0])
                                if (x < bbox_x + bbox_w and x + w > bbox_x and
                                        y < bbox_y + bbox_h and y + h > bbox_y):
                                    # Expand the bounding box to contain the face
                                    x = min(x, bbox_x)
                                    y = min(y, bbox_y)
                                    w = max(x + w, bbox_x + bbox_w) - x
                                    h = max(y + h, bbox_y + bbox_h) - y

                                    # Initialize face tracking if not already started
                                    if not face_detected:
                                        face_tracker.init(frame, (x, y, w, h))
                                        face_detected = True
                                    else:
                                        # Update the face tracker
                                        success, face_box = face_tracker.update(frame)
                                        if success:
                                            (x, y, w, h) = [int(c) for c in face_box]

            else:
                # Save the initial object bounding box
                object_bbox = (x, y, w, h)
                object_tracking = True

            # Draw the bounding box on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 0, 100), 2)

    # Process the frame with Mediapipe hand pose estimation
    results_hands = mp_hands.process(frame_rgb)

    # Check if hands were detected
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # Convert hand landmarks to integer points
            hand_points = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in hand_landmarks.landmark]

            # Get the bounding box coordinates of the hand
            hand_bbox = cv2.boundingRect(np.array(hand_points))

            # Draw hand landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow('Object Tracking and Hand Pose Estimation', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the windows
cap.release()
cv2.destroyAllWindows()

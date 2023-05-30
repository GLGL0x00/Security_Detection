import tkinter as tk
import cv2
from PIL import Image, ImageTk
from trainner import trainner
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
model = YOLO("bestface.pt")
#
# def nav():
#     messagebox.showinfo("restart ")
#
# def videocapture():
#     window = tk.Tk()
#     window.title("Capture photos" )
#     window_width = 800
#     window_height = 600
#     window.geometry(f"{window_width}x{window_height}")
#     # webcame label
#     webcam_label = tk.Label(window)
#     webcam_label.pack()
#     # Create a label to display the counter
#     counter_label = tk.Label(window, text="50")
#     counter_label.pack()
#     # Create a button to navigate to another function
#     navigate_button = tk.Button(window, text="Restart", command=nav)
#     navigate_button.pack()
#     counter = 50
#
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#
#     if ret:
#         # Convert the frame to PIL format
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image = Image.fromarray(image)
#
#         # Resize the image to fit the label
#         image = image.resize((400, 300))
#
#         # Convert the image to Tkinter PhotoImage
#         photo = ImageTk.PhotoImage(image)
#
#         # Update the label with the new image
#         webcam_label.config(image=photo)
#         webcam_label.image = photo
#         counter_label.config(text=str(counter))
#         counter -= 1
#         if counter >= 0:
#             # Schedule the next update after 1 second
#             window.after(1000, update_webcam)
#         else:
#             # Release the camera
#             self.cap.release()
#     window.mainloop()
#
# videocapture()




cap = cv2.VideoCapture(0)
def update_webcam(cap):
    global counter
    # Read a frame from the webcam
    ret, frame = cap.read()

    if ret:

        # Convert the frame to PIL format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(image)

        # Resize the image to fit the label
        image = image.resize((600, 400))

        # Convert the image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        webcam_label.config(image=photo)
        webcam_label.image = photo

    # Update the counter label
    counter_label.config(text=str(counter))

    # Decrease the counter by 1
    counter -= 1

    if counter >= 0:
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = model.predict(frame)
        for r in result:
            annotator = Annotator(frame)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                annotator.box_label(b, model.names[int(c)], 3)
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                cv2.rectangle(frame, (x, y), (w, h), (100, 100, 0), 2)

                cv2.imwrite('dataset/User.' + str(counter) + '.jpg', grayImage[:y + h, :x + w])
                print("savephoto")
        # Schedule the next update after 1 second
        root.after(2000, update_webcam, cap)
    else:
        trainner()
        # Release the camera
        cap.release()
        webcam_label.destroy()

def navigate():
    # Add your code here for the navigation functionality
    print("Navigating to another function")

root = tk.Tk()
root.title("Capture Photo" )
root.configure(bg="#593825")
root.geometry("800x600")

# Create a label to display the webcam view
webcam_label = tk.Label(root , bd=0, relief="flat")
webcam_label.pack(pady=10)

# Create a label to display the counter
counter_label = tk.Label(root, text="50",font="7")
counter_label.pack(pady=5)

# Create a button to navigate to another function
navigate_button = tk.Button(root, text="Re-Start", bg="#1A333A", fg="white",width=20,command=navigate)
navigate_button.pack(pady=5)

# Initialize the counter value
counter = 5

# Start the webcam
update_webcam(cap)
root.mainloop()

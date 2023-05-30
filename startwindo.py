import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint
import json
import cv2
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
model = YOLO("bestface.pt")
def navigate_to_next_page(name):
    getname = name.get()
    if getname and not (getname.isdigit()):

        # Do something with the entered name
        Id = randint(0, 100)
        with open("users.json") as json_file:
            data = json.load(json_file)

        username = {
            'name': getname
        }
        data[Id] = username

        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)

        video()
    else:
        messagebox.showwarning("Error", "Please enter a name.")

def createstartwindow():

    # Create the main window
    window = tk.Tk()
    window.title("Add New Person " )
    window_width = 800
    window_height = 600
    window.geometry(f"{window_width}x{window_height}")
    # set bg
    image = Image.open(r"D:\4th Year\detect and website\yolov8\static\img\OIG.jpg")
    image = image.resize((800, 600))  # Set the desired width and height
    background_image = ImageTk.PhotoImage(image)
    # Create a label for the background image
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Calculate the center position of the window
    center_x = window_width // 2
    center_y = window_height // 2
    container_width = 300
    container_height = 150

    # Calculate the position of the LabelFrame
    container_x = center_x - (container_width // 2)
    container_y = center_y - (container_height // 2)

    container=tk.Frame(background_label ,bg="")
    container.place(x=container_x, y=container_y, width=container_width, height=container_height)

    # Create a label and entry field for the name
    name_label = tk.Label(container, text="Enter your name:",width=16, font="8", bg="#1A333A",fg="white")
    name_label.pack(pady=10)

    name_entry = tk.Entry(container , width=16 ,font="4")
    name_entry.pack(pady=10)

    # Create a button to navigate to the next page
    next_button = tk.Button(container , text="Start", bg="#1A333A", fg="white", command=lambda: navigate_to_next_page(name_entry),width=20)
    next_button.pack(pady=10)


    # Start the GUI event loop
    window.mainloop()

def update_webcam(cap, root, webcam_label, counter_label):
    global counter

    # Read a frame from the webcam
    ret, frame = cap.read()

    if ret:
        # Convert the frame to PIL format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Resize the image to fit the label
        image = image.resize((600, 400))
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        webcam_label.config(image=photo)
        webcam_label.image = photo
        # # Convert the image to Tkinter PhotoImage
        # photo = ImageTk.PhotoImage(image)
        #
        # # Update the label with the new image
        # webcam_label.config(image=photo)
        # webcam_label.image = photo  # Store the PhotoImage to prevent garbage collection

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
        # Schedule the next update after 1 second
        root.after(1000, update_webcam, cap, root, webcam_label, counter_label)
    else:
        # Release the camera
        cap.release()
        webcam_label.destroy()


def video():

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
    navigate_button = tk.Button(root, text="Re-Start", bg="#1A333A", fg="white",width=20,command=createstartwindow)
    navigate_button.pack(pady=5)

    # Initialize the counter value
    counter = 5
    # start webcam

    cap = cv2.VideoCapture(0)
    update_webcam(cap,root,webcam_label,counter_label)
    root.mainloop()

createstartwindow()



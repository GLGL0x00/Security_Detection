import tkinter as tk
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint
import json
import cv2
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
from trainner import trainner

model = YOLO("bestface.pt")


def createstartwindow():
    def navigate_to_next_page(name):
        itr = 0
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
            window.destroy()
            camera = cv2.VideoCapture(0)
            while 1:

                _, image = camera.read()

                grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # face = cascade.detectMultiScale(grayImage,
                #                                 scaleFactor = 1.5,
                #                                 minNeighbors = 5,
                #                                 minSize= (30,30))

                result = model.predict(image)
                for r in result:
                    annotator = Annotator(image)
                    boxes = r.boxes
                    for box in boxes:
                        b = box.xyxy[0]
                        c = box.cls
                        annotator.box_label(b, model.names[int(c)], 3)
                        x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                        cv2.rectangle(image, (x, y), (w, h), (100, 100, 0), 2)

                        cv2.imwrite('dataset/User.' + str(Id) + '.' + str(itr) + '.jpg', grayImage[:y + h, :x + w])

                itr += 1

                if itr == 51:
                    break

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break

                cv2.imshow('Frame', image)
            camera.release()
            cv2.destroyAllWindows()
            trainner()
        else:
            messagebox.showwarning("Error", "Please enter a name.")

    # Create the main window
    window = customtkinter.CTk()
    window.title("Add New Person " )
    window_width = 200
    window_height = 100
    window.geometry(f"{window_width}x{window_height}")



    container=customtkinter.CTkFrame(window)
    container.pack()
    # Create a label and entry field for the name
    name_label = customtkinter.CTkLabel(container, text="Enter your name:",width=16)
    name_label.pack()

    name_entry = customtkinter.CTkEntry(container)
    name_entry.pack()

    # Create a button to navigate to the next page
    next_button = customtkinter.CTkButton(container , text="Start", command=lambda: navigate_to_next_page(name_entry))
    next_button.pack()


    # Start the GUI event loop
    window.mainloop()

# def update_webcam(cap, window, webcam_label, counter_label):
#     global counter
#
#     # Read a frame from the webcam
#     ret, frame = cap.read()
#
#     if ret:
#         # Convert the frame to PIL format
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image = Image.fromarray(image)
#
#         # Resize the image to fit the label
#         image = image.resize((600, 400))
#         photo = ImageTk.PhotoImage(image)
#
#         # Update the label with the new image
#         webcam_label.config(image=photo)
#         webcam_label.image = photo
#         # # Convert the image to Tkinter PhotoImage
#         # photo = ImageTk.PhotoImage(image)
#         #
#         # # Update the label with the new image
#         # webcam_label.config(image=photo)
#         # webcam_label.image = photo  # Store the PhotoImage to prevent garbage collection
#
#     # Update the counter label
#     counter_label.config(text=str(counter))
#
#     # Decrease the counter by 1
#     counter -= 1
#
#     if counter >= 0:
#         grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         result = model.predict(frame)
#         for r in result:
#             annotator = Annotator(frame)
#             boxes = r.boxes
#             for box in boxes:
#                 b = box.xyxy[0]
#                 c = box.cls
#                 annotator.box_label(b, model.names[int(c)], 3)
#                 x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
#                 cv2.rectangle(frame, (x, y), (w, h), (100, 100, 0), 2)
#
#                 cv2.imwrite('dataset/User.' + str(counter) + '.jpg', grayImage[:y + h, :x + w])
#         # Schedule the next update after 1 second
#         window.after(1000, update_webcam, cap, window, webcam_label, counter_label)
#     else:
#         # Release the camera
#         cap.release()
#         webcam_label.destroy()
#
#
# def video():
#
#
#     window = tk.Tk()
#     window.title("Capture Photo" )
#     window.configure(bg="#593825")
#     window.geometry("800x600")
#
#     # Create a label to display the webcam view
#     webcam_label = tk.Label(window , bd=0, relief="flat")
#     webcam_label.pack(pady=10)
#
#     # Create a label to display the counter
#     counter_label = tk.Label(window, text="50",font="7")
#     counter_label.pack(pady=5)
#
#     # Create a button to navigate to another function
#     navigate_button = tk.Button(window, text="Re-Start", bg="#1A333A", fg="white",width=20,command=createstartwindow)
#     navigate_button.pack(pady=5)
#
#     # Initialize the counter value
#     counter = 5
#     # start webcam
#
#     cap = cv2.VideoCapture(0)
#     update_webcam(cap,window,webcam_label,counter_label)
#     window.mainloop()
#
# createstartwindow()
# video()



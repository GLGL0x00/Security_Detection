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
    def navigate_to_next_page(name, status):
        itr = 0
        getname = name.get()
        if getname and not (getname.isdigit()):

            # Do something with the entered name
            Id = randint(0, 100)
            with open("users.json") as json_file:
                data = json.load(json_file)

            username = {
                'name': getname,
                'mode': status
            }
            data[Id] = username

            with open("users.json", "w") as file:
                json.dump(data, file, indent=4)
            window.destroy()
            camera = cv2.VideoCapture(0)
            while 1:

                _, image = camera.read()

                grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


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

    check_var = tk.StringVar(value="Not Allowed")
    checkbox = customtkinter.CTkCheckBox(master=window,text="Allow?",
                                        variable=check_var, onvalue="Allowed", offvalue="Not Allowed")
    checkbox.pack(pady = 5, padx = 10)

    # Create a button to navigate to the next page
    next_button = customtkinter.CTkButton(container , text="Start", command=lambda: navigate_to_next_page(name_entry, check_var.get()))
    next_button.pack()


    # Start the GUI event loop
    window.mainloop()


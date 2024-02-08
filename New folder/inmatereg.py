import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
import tkinter as tk
import random
import time
from datetime import datetime
from tkinter import messagebox
import mysql.connector as mycon
from mysql.connector import Error
import torch


# Create a directory for storing face images and annotations
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Create directories for images and labels if they don't exist
if not os.path.exists('dataset/images'):
    os.makedirs('dataset/images')
if not os.path.exists('dataset/labels'):
    os.makedirs('dataset/labels')

model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'C:\Users\Niels\Desktop\Programming\YOLOV5\yolov5sfacetrained.pt')

# Initialize ID counter
id_counter = 0

# Create an empty list to store class names dynamically
class_names = []

# Set the time interval for capturing images (in seconds)
capture_interval = 1  # Capture an image every 1 second
last_capture_time = 0

# Limitation of generated picture
max_picture = 20



root = Tk()
root.title("Inmate Registration System")
root.geometry("1180x620+210+100")
root.config(bg = "#ffffff")

lbltitle = Label(root,text="INMATE REGISTRATION", width = 10, height = 2, bg = "#07bdff", fg ='#fff', font = 'Arial 20 bold').pack(side = TOP, fill = X)

		######### Inmate Registration Frame #################

regframe = LabelFrame(root, text = "Inmate's Details", font = 20, bd = 2, width = 730, height = 500, relief = RIDGE)
regframe.place(x = 20, y = 80)

		################ Photo Frame ######################

photoframe = LabelFrame(root, text = "Scan Photo", font = 20, bd = 2, width = 347, height = 500, relief = RIDGE)
photoframe.place(x = 800, y = 80)

		########## Labels in Registration Frame

lblInmate = Label(regframe, text = "Inmate No.:", font = ("arial", 13,"bold")).place(x = 30, y = 50)
lblDOB = Label(regframe, text = "Date of Birth:", font = ("arial", 13,"bold")).place(x = 30, y = 140)
lblGender = Label(regframe, text = "Gender:", font = ("arial", 13,"bold")).place(x = 30, y = 230)

lblAdd = Label(regframe, text = "Address:", font = ("arial", 13,"bold")).place(x = 500, y = 50)
lblCont = Label(regframe, text = "Contact No.:", font = ("arial", 13,"bold")).place(x = 500, y = 140)
lblNat = Label(regframe, text = "Nationality:", font = ("arial", 13,"bold")).place(x = 500, y = 230)

		########### Enter Data ##############

Inmateno = StringVar()
inmate_entry = Entry(regframe, textvariable = Inmateno, width = 20, font = "arial 10")
inmate_entry.place(x = 30, y = 80)

DateOB = StringVar()
date_of_birth_entry = Entry(regframe, textvariable = DateOB, width = 20, font = "arial 10")
date_of_birth_entry.place(x = 30, y = 170)

Address = StringVar()
add_entry = Entry(regframe, textvariable = Address, width = 20, font = "arial 10")
add_entry.place(x = 500, y = 80)

Contact = StringVar()
cont_entry = Entry(regframe, textvariable = Contact, width = 20, font = "arial 10")
cont_entry.place(x = 500, y = 170)

Nationality = StringVar()
nat_entry = Entry(regframe, textvariable = Nationality, width = 20, font = "arial 10")
nat_entry.place(x = 500, y = 260)

gender_var = StringVar()
gender_options = ['Male', 'Female', 'Non-Binary', 'Other']
gender_var.set(gender_options[0])  # Set default value
gender_menu = OptionMenu(regframe, gender_var, *gender_options)
gender_menu.place(x = 30, y = 260)


def nextPage():
    root.destroy()
    import inmateprofile

def nextPage1():
	root.destroy()
	import inmatelist

########## FUNCTIONS ###############

def Clear():
	Inmateno.set('')
	DateOB.set('')
	Address.set('')
	Contact.set('')
	Nationality.set('')
	gender_var.set('')

########## DATABASE ###############

def save_info():
    inmate_no = inmate_entry.get()
    date_of_birth = date_of_birth_entry.get()
    gender = gender_var.get()
    address = add_entry.get()
    cont_number = cont_entry.get()
    nationality = nat_entry.get()
    mydb = mycon.connect(host="localhost", user="root", password="", database="cvtest") #connection
    mycursor = mydb.cursor(buffered=True)  #after connection
    # Check for duplicate names in the database
    mycursor.execute("SELECT * FROM Detainees WHERE inmate_no = %s AND date_of_birth = %s", (inmate_no, date_of_birth))
    existing_profile = mycursor.fetchone()
    if existing_profile:
        messagebox.showerror("Error", "Profile already registered")
        mydb.commit()
        mydb.close()
        return
    else:
        insert_query = "INSERT INTO Detainees (inmate_no, date_of_birth, gender, address, phone_number, nationality) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (inmate_no, date_of_birth, gender, address, cont_number, nationality)  # Add values for other fields
        mycursor.execute(insert_query, values)
    mydb.commit()
    mydb.close()
    
    # Execute the insert query using your MySQL connection here
    
    messagebox.showinfo("Success", "Information saved to database.")

def capture_face():
    global id_counter, last_capture_time

    # Open webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Set the width (3) to 640 pixels
    cap.set(4, 640)  # Set the height (4) to 640 pixels

    frame_count = 0
    start_time = time.time()

    # Set a minimum confidence threshold for detections
    min_confidence = 0.5  # Adjust this value as needed

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 640))
        if not ret:
            break

        current_time = datetime.now()
        

        if current_time.timestamp() - last_capture_time >= capture_interval:
            results = model(frame)  # Perform inference with the model
            detections = []

            for _, det in enumerate(results.pred[0]):
                conf, cls, xyxy = det[4], int(det[5]), det[0:4]
                if conf >= min_confidence:  # 
                    x1, y1, x2, y2 = map(int, xyxy)
                    detections.append([x1, y1, x2, y2])

                # Draw bounding boxes around detected persons
                for det in detections:
                    x1, y1, x2, y2 = det
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Save the detected face
                face_image_filename = os.path.join('dataset/images', f'{id_counter}_{int(current_time.timestamp())}.jpg')
                cv2.imwrite(face_image_filename, frame)

                # Save bounding box annotation in Darknet format
                annotation_filename = os.path.join('dataset/labels', f'{id_counter}_{int(current_time.timestamp())}.txt')
                with open(annotation_filename, 'w') as f:
                    for det in detections:
                        x1, y1, x2, y2 = det
                        # Convert the coordinates to Darknet format
                        width = frame.shape[1]
                        height = frame.shape[0]
                        x_center = (x1 + x2) / (2 * width)
                        y_center = (y1 + y2) / (2 * height)
                        bbox_width = (x2 - x1) / width
                        bbox_height = (y2 - y1) / height
                        f.write(f'0 {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n')

                        elapsed_time = time.time() - start_time

                        


            # Calculate and display FPS
            fps = frame_count / elapsed_time
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("Capture", frame)

        frame_count += 1
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Face images for profile {id_counter} captured and saved.")


		########## Inmate Buttons ############

btnSave = Button(regframe, text = "Save", width = 19, height = 2, font = "arial 12 bold", bg = "lightblue", command=save_info)
btnSave.place(x = 90, y = 320)

btnClear = Button(regframe, text = "Clear", width = 19, height = 2, font = "arial 12 bold", bg = "lightblue", command=Clear)
btnClear.place(x = 400, y = 320)


		######## Photo Upload ########

photof = Frame(photoframe, bd = 3, bg = "black", width = 160, height = 140, relief = RIDGE)
photof.place(x = 90, y = 50)

img = PhotoImage(file = "C:/Thesis/Wes/camera.png")
lbl = Label(photoframe, bg = "blue", image = img)
lbl.place(x = 20000, y = 80)



		######### Photo Frame Buttons ########

btnProfile = Button(photoframe, text = "Profile", width = 19, height = 2, font = "arial 12 bold", bg = "lightblue", command=nextPage)
btnProfile.place(x = 70, y = 300)
btnList = Button(photoframe, text = "List", width = 19, height = 2, font = "arial 12 bold", bg = "lightblue", command=nextPage1)
btnList.place(x = 70, y = 380)
btnScan = Button(photoframe, text = "Scan", width = 19, height = 2, font = "arial 12 bold", bg = "lightblue", command=capture_face).place(x = 70, y = 220)
	

root.mainloop()


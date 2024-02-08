import cv2
import os
import tkinter as tk
from tkinter import messagebox
from mtcnn import MTCNN
from datetime import datetime
import time
import mysql.connector as mycon
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from skimage import io, color, feature
import csv


# Create a directory for storing face images and annotations
if not os.path.exists('dataset'):
    os.makedirs('dataset')
if not os.path.exists('dataset/images'):
    os.makedirs('dataset/images')
if not os.path.exists('dataset/labels'):
    os.makedirs('dataset/labels')
if not os.path.exists('dataset/lbp'):
    os.makedirs('dataset/lbp')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize ID counter
id_counter = 0

# Set the time interval for capturing images (in seconds)
capture_interval = 1  # Capture an image every 1 second
last_capture_time = 0

# Limitation of generated picture
max_picture = 20

# Create an empty list to store class names dynamically
class_names = []

# Lists to store labels and features for LBP
lbp_labels = []
lbp_features = []

# Create Tkinter window
window = tk.Tk()
window.title("Face Registration")

# Function to capture and save face images
def submit_info():
    global merged_name
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    dob = dob_entry.get()
    gender = gender_var.get()
    address = address_entry.get()
    phone_number = phone_entry.get()
    email = email_entry.get()
    nationality = nationality_entry.get()
    
    # Use marital_var for marital_status
    marital_status = marital_var.get()
    
    occupation = occupation_entry.get()
    merged_name = f"{first_name} {last_name}"
    
    mydb = mycon.connect(host="localhost", user="root", password="", database="cvtest")  # connection
    mycursor = mydb.cursor(buffered=True)  # after connection
    
    # Check for duplicate names in the database
    mycursor.execute("SELECT * FROM Detainees WHERE first_name = %s AND last_name = %s", (first_name, last_name))
    existing_profile = mycursor.fetchone()
    
    if existing_profile:
        messagebox.showerror("Error", "Profile already registered")
        return
    else:
        insert_query = "INSERT INTO Detainees (first_name, last_name, date_of_birth, gender, address, phone_number, email, nationality, marital_status, occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (first_name, last_name, dob, gender, address, phone_number, email, nationality, marital_status, occupation)  # Add values for other fields
        mycursor.execute(insert_query, values)
    
    mydb.commit()
    mydb.close()

    # Append the class name to the dynamic class_names list
    if merged_name not in class_names:
        class_names.append(merged_name)
        print("Current class_names:", class_names)

        # Before checking for the train/test split
        print("Unique classes:", len(set(class_names)))

    # Execute the insert query using your MySQL connection here
    messagebox.showinfo("Success", "Information saved to the database.")

def capture_face():
    global id_counter, last_capture_time  # Use the global variables

    clean_name = ''.join(char if ord(char) < 128 else '_' for char in merged_name)

    cap = cv2.VideoCapture(0)

    frame_count = 0
    start_time = time.time()

    # Initialize MTCNN for facial landmark detection
    detector = MTCNN()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = datetime.now()

        if current_time.timestamp() - last_capture_time >= capture_interval:
            # Convert frame to grayscale for Haar Cascade
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces using Haar Cascade
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            lbp_data = []

            # Draw rectangles around detected faces and facial landmarks
            for (x, y, width, height) in faces:
                cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)

                # Add a margin around the detected face
                margin = 75
                x = max(0, x - margin)
                y = max(0, y - margin)
                width += 2 * margin
                height += 2 * margin

                # Extract face region
                face_region = gray[y:y+height, x:x+width]

                # Detect facial landmarks using MTCNN
                detections = detector.detect_faces(frame)
                if detections:
                    facial_landmarks = detections[0]['keypoints']
                    
                    # Draw facial landmarks (for illustration purposes)
                    for point in facial_landmarks.values():
                        cv2.circle(frame, tuple(map(int, point)), 2, (0, 255, 0), -1)

                # Apply LBP feature extraction
                lbp_features = feature.local_binary_pattern(face_region, P=8, R=1, method="uniform")

                # Save LBP features and label to the list
                lbp_data.append({'label': merged_name, 'features': lbp_features.flatten().tolist()})
                cv2.imshow("Frame", frame)
                cv2.waitKey(1)

                # Draw facial landmarks (for illustration only, not saved)
                landmarks = facial_landmarks(face_region)
                for landmark in landmarks:
                    cv2.circle(frame, (int(x + landmark[0]), int(y + landmark[1])), 1, (0, 0, 255), -1)

            # Save LBP features and labels to a list
            lbp_labels.extend([sample['label'] for sample in lbp_data])
            lbp_features.extend([sample['features'] for sample in lbp_data])

            # Display the frame
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

            # Update last_capture_time
            last_capture_time = current_time.timestamp()

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Face images for {merged_name} captured and saved.")


def process_data(dataset_path, lbp_path):
    lbp_features_list = []
    labels_list = []

    for filename in os.listdir(dataset_path):
        if filename.endswith(".jpg"):
            merged_name = filename.split('_')[0]
            labels_list.append(merged_name)

            image_path = os.path.join(dataset_path, filename)
            img = io.imread(image_path, as_gray=True)

            # Extract LBP features
            lbp = feature.local_binary_pattern(img, P=8, R=1, method="uniform")
            lbp_features_list.append(lbp.flatten())

    # Convert lists to numpy arrays
    lbp_features = np.array(lbp_features_list)
    labels = np.array(labels_list)

    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)

    return lbp_features, encoded_labels

def train_test_data():
    # Call prepare_train_test_data after capturing face images
    X_train, X_test, y_train, y_test = prepare_data()

def prepare_data():
    global lbp_labels, lbp_features

    if len(class_names) < 2:
        messagebox.showerror("Error", "Not enough samples for train/test split.")
        return None, None, None, None

    # Convert lists to numpy arrays
    lbp_labels = np.array(lbp_labels)
    lbp_features = np.array(lbp_features)

    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(lbp_labels)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(lbp_features, encoded_labels, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


#Left side label
tk.Label(window, text="First Name:").grid(row=0, column=0, sticky='w')
first_name_entry = tk.Entry(window)
first_name_entry.grid(row=0, column=1, sticky='w')

tk.Label(window, text="Last Name:").grid(row=1, column=0, sticky='w')
last_name_entry = tk.Entry(window)
last_name_entry.grid(row=1, column=1, sticky='w')

tk.Label(window, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, sticky='w')
dob_entry = tk.Entry(window)
dob_entry.grid(row=2, column=1, sticky='w')

tk.Label(window, text="Gender:").grid(row=3, column=0, sticky='w')
gender_options = ['Male', 'Female', 'Non-Binary', 'Other']
gender_var = tk.StringVar(window)
gender_var.set(gender_options[0])  # Set default value
gender_menu = tk.OptionMenu(window, gender_var, *gender_options)
gender_menu.grid(row=3, column=1, sticky='w')

tk.Label(window, text="Address:").grid(row=4, column=0, sticky='w')
address_entry = tk.Entry(window)
address_entry.grid(row=4, column=1, sticky='w')

tk.Label(window, text="Contact Number:").grid(row=5, column=0, sticky='w')
phone_entry = tk.Entry(window)
phone_entry.grid(row=5, column=1, sticky='w')

tk.Label(window, text="Email:").grid(row=6, column=0, sticky='w')
email_entry = tk.Entry(window)
email_entry.grid(row=6, column=1, sticky='w')

# Create and pack labels and entry widgets for the right side
tk.Label(window, text="Nationality:").grid(row=0, column=2, sticky='w')
nationality_entry = tk.Entry(window)
nationality_entry.grid(row=0, column=3, sticky='w')

tk.Label(window, text="Marital Status:").grid(row=1, column=2, sticky='w')
marital_options = ['Single', 'Married', 'Divorced', 'Widowed', 'Other']
marital_var = tk.StringVar(window)
marital_var.set(marital_options[0])  # Set default value
marital_menu = tk.OptionMenu(window, marital_var, *marital_options)
marital_menu.grid(row=1, column=3, sticky='w')

tk.Label(window, text="Occupation:").grid(row=2, column=2, sticky='w')
occupation_entry = tk.Entry(window)
occupation_entry.grid(row=2, column=3, sticky='w')

submit_button = tk.Button(window, text="Submit", command=submit_info)
submit_button.grid(row=7, column=2, columnspan=2, sticky='w')

# Create and pack the "Scan" button
scan_button = tk.Button(window, text="Scan", command=capture_face)
scan_button.grid(row=8, column=2, columnspan=2, sticky='w')

train_test_button = tk.Button(window, text="Train/Test Data", command=train_test_data)
train_test_button.grid(row=9, column=2, columnspan=2, sticky='w')

# Create the frame for video display
frame_display = tk.Frame(window, width=640, height=480)
frame_display.grid(row=0, column=2, rowspan=3)

# Start the Tkinter main loop
window.mainloop()

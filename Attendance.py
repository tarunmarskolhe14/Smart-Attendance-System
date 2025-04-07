import cv2
import os
import numpy as np
import pickle
from datetime import datetime
import pandas as pd

# Generate a unique timestamp for file names
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Paths with unique filenames
model_path = r"D:\Project\face_recognition_project\trained_model.yml"
labels_path = r"D:\Project\face_recognition_project\labels.pkl"
haar_path = r"D:\Project\face_recognition_project\haarcascade_frontalface_default.xml"
output_excel = f"D:\\Project\\face_recognition_project\\attendance_{timestamp}.xlsx"
output_csv = f"D:\\Project\\face_recognition_project\\attendance_{timestamp}.csv"

# Check if paths exist
if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}")
    exit()
if not os.path.exists(labels_path):
    print(f"Error: Labels file not found at {labels_path}")
    exit()
if not os.path.exists(haar_path):
    print(f"Error: Haar cascade XML file not found at {haar_path}")
    exit()

# Load Haar cascade and recognizer
face_cascade = cv2.CascadeClassifier(haar_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Check if model loading is successful
if not os.path.exists(model_path):
    print(f"Error: Trained model not found at {model_path}")
    exit()

recognizer.read(model_path)

# Load label mapping
try:
    with open(labels_path, 'rb') as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}  # Reverse mapping: ID -> Name
except Exception as e:
    print(f"Error: Failed to load labels from {labels_path}. {e}")
    exit()

# To store who is already marked present
attendance_set = set()

# Create a DataFrame to store attendance logs with Serial No
attendance_df = pd.DataFrame(columns=["Serial No", "Name", "Date", "Time", "Status"])

# Open webcam
cap = cv2.VideoCapture(0)

# Check if webcam is opened
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

serial_no = 1  # Start serial number from 1

print("Starting face recognition. Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]

        # Predict
        id_, conf = recognizer.predict(roi_gray)
        if conf < 70:  # Confidence threshold (lower = better)
            name = labels.get(id_, "Unknown")

            # If not already marked
            if name not in attendance_set:
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                # Add row with Serial No
                new_row = pd.DataFrame([{
                    "Serial No": serial_no,
                    "Name": name,
                    "Date": date_str,
                    "Time": time_str,
                    "Status": "Present"  # Add "Present" status here
                }])
                attendance_df = pd.concat([attendance_df, new_row], ignore_index=True)
                attendance_set.add(name)

                # Increment serial number
                serial_no += 1

                # Updated log message to show "Present"
                print(f"[PRESENT] {name} at {time_str}")

            # Draw label on face
            cv2.putText(frame, name, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 0, 255), 2)

    # Show the video feed
    cv2.imshow("Face Recognition Attendance", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save to Excel and CSV
if not attendance_df.empty:
    try:
        attendance_df.to_excel(output_excel, index=False)
        attendance_df.to_csv(output_csv, index=False)
        print(f"✅ Attendance saved to: {output_excel}")
        print(f"✅ Attendance also saved to: {output_csv}")
    except Exception as e:
        print(f"Error: Failed to save attendance. {e}")
else:
    print("No attendance to save.")

cap.release()
cv2.destroyAllWindows()

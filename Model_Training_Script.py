import cv2
import os
import numpy as np

# Path to the dataset
dataset_path = r"D:\Project\face_recognition_project\dataset"
haar_cascade_path = r"D:\Project\face_recognition_project\haarcascade_frontalface_default.xml"

# Initialize face detector
face_cascade = cv2.CascadeClassifier(haar_cascade_path)

# Face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
faces = []
labels = []

print("Preparing training data...")

# Loop through dataset folders
for root, dirs, files in os.walk(dataset_path):
    for dir_name in dirs:
        person_path = os.path.join(root, dir_name)
        label = dir_name

        if label not in label_ids:
            label_ids[label] = current_id
            current_id += 1

        for image_name in os.listdir(person_path):
            img_path = os.path.join(person_path, image_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            # Detect face
            faces_rect = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces_rect:
                roi = img[y:y+h, x:x+w]
                faces.append(roi)
                labels.append(label_ids[label])

# Train the model
print("Training model...")
recognizer.train(faces, np.array(labels))

# Save the trained model
model_path = r"D:\Project\face_recognition_project\trained_model.yml"
recognizer.save(model_path)

# Optionally save label mapping
import pickle
with open("labels.pkl", "wb") as f:
    pickle.dump(label_ids, f)

print(f"Model trained and saved to {model_path}")

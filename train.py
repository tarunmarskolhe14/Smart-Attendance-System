from utils import create_dataset, save_model
import cv2 as cv
import numpy as np

print("[INFO] Creating dataset...")
features, labels = create_dataset('dataset')

features = np.array(features, dtype='object')
labels = np.array(labels)

print("[INFO] Training model...")
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(features, labels)

save_model(face_recognizer, features, labels)
print("[SUCCESS] Training complete and model saved.")

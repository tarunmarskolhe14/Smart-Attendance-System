import cv2
import os
import time
from datetime import datetime

# Base dataset path
base_path = r"D:\Project\face_recognition_project\dataset"

# Ask for folder name
folder_name = input("Enter folder name to save or reuse: ")
target_folder = os.path.join(base_path, folder_name)

# Check if folder exists
if os.path.exists(target_folder):
    choice = input(f"Folder '{folder_name}' already exists. Do you want to reuse it? (y/n): ").lower()
    if choice != 'y':
        folder_name = input("Enter a new folder name: ")
        target_folder = os.path.join(base_path, folder_name)

# Create the final folder
os.makedirs(target_folder, exist_ok=True)
print(f"Saving images to: {target_folder}")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

img_count = 0
print("Capturing images continuously. Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame.")
        break

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(target_folder, f"img_{img_count}_{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Captured: {filename}")
    img_count += 1

    # Display the frame
    cv2.imshow("Capturing... Press 'q' to stop", frame)

    # Wait 1 second and listen for 'q'
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        print("Stopping capture.")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()


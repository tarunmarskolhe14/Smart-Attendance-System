import os
import pandas as pd

# Change this to your attendance directory
attendance_dir = r"D:\Project\face_recognition_project"

def list_attendance_files():
    files = []
    for f in os.listdir(attendance_dir):
        if f.endswith(".csv") or f.endswith(".xlsx"):
            files.append(f)
    return files

def view_file(file_name):
    file_path = os.path.join(attendance_dir, file_name)
    print(f"\n Viewing file: {file_name}\n{'-'*40}")
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format.")
            return
        print(df.to_string(index=False))
    except Exception as e:
        print(f" Error reading file: {e}")

def main():
    files = list_attendance_files()
    if not files:
        print("No attendance files (.csv or .xlsx) found.")
        return

    print(" Attendance Files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("Select a file number to view: "))
        if 1 <= choice <= len(files):
            view_file(files[choice - 1])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()

import os
import glob

def delete_yml():
    yml_file = r"D:\Project\face_recognition_project\trained_model.yml"
    if os.path.exists(yml_file):
        print(f"\nFound: {yml_file}")
        confirm = input("Do you want to delete this .yml file? (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                os.remove(yml_file)
                print(f"Deleted: {yml_file}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Skipped.")
    else:
        print("No .yml file found.")

def delete_xlsx():
    folder_path = r"D:\Project\face_recognition_project"
    xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
    if not xlsx_files:
        print("No .xlsx files found.")
        return
    for file_path in xlsx_files:
        choice = input(f"\nDelete this file?\n{file_path} (yes/no): ").strip().lower()
        if choice == 'yes':
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Skipped.")

def delete_csv():
    folder_path = r"D:\Project\face_recognition_project"
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_files:
        print("No .csv files found.")
        return
    for file_path in csv_files:
        choice = input(f"\nDelete this file?\n{file_path} (yes/no): ").strip().lower()
        if choice == 'yes':
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Skipped.")

# Function to delete all .xlsx files without prompt
def delete_all_xlsx():
    folder_path = r"D:\Project\face_recognition_project"
    xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
    if not xlsx_files:
        print("No .xlsx files to delete.")
        return
    for file_path in xlsx_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Function to delete all .csv files without prompt
def delete_all_csv():
    folder_path = r"D:\Project\face_recognition_project"
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_files:
        print("No .csv files to delete.")
        return
    for file_path in csv_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def delete_images():
    dataset_root = r"D:\Project\face_recognition_project\dataset"
    subfolders = [name for name in os.listdir(dataset_root)
                  if os.path.isdir(os.path.join(dataset_root, name))]

    if not subfolders:
        print("No folders found in dataset.")
        return

    print("\nFolders inside dataset:")
    for i, folder in enumerate(subfolders, 1):
        print(f"{i}. {folder}")
    try:
        choice = int(input("Enter the number of the folder to clean images from: "))
        selected_folder = subfolders[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    folder_path = os.path.join(dataset_root, selected_folder)
    image_extensions = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(folder_path, ext)))

    print(f"\nFolder: {selected_folder}")
    print(f"Found {len(image_paths)} image(s).")
    if image_paths:
        print("Preview:")
        print("\n".join(image_paths[:5]))
        if len(image_paths) > 5:
            print("...")

    confirm = input(f"\nDelete ALL images in '{selected_folder}'? Type 'yes' to confirm: ").strip().lower()
    if confirm == "yes":
        deleted = 0
        for img in image_paths:
            try:
                os.remove(img)
                deleted += 1
            except Exception as e:
                print(f"Error deleting {img}: {e}")
        print(f"Deleted {deleted} image(s).")
    else:
        print("Deletion cancelled.")

def main():
    while True:
        print("\nSelect file type to delete:")
        print("1. .yml file")
        print("2. .xlsx file(s) (with confirmation)")
        print("3. Image files (from dataset folder)")
        print("4. .csv file(s) (with confirmation)")
        print("5. Delete ALL .xlsx files (no confirmation)")
        print("6. Delete ALL .csv files (no confirmation)")
        print("7. Exit")

        option = input("Enter choice (1-7): ").strip()

        if option == '1':
            delete_yml()
        elif option == '2':
            delete_xlsx()
        elif option == '3':
            delete_images()
        elif option == '4':
            delete_csv()
        elif option == '5':
            delete_all_xlsx()
        elif option == '6':
            delete_all_csv()
        elif option == '7':
            print("Exiting. Have a great day!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

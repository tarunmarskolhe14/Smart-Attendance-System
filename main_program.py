import subprocess
import os
import getpass

# Set paths to all your scripts
scripts = {
    "registration": "Student's-registration.py",
    "training": "Model_Training_Script.py",
    "attendance": "Attendance.py",
    "view": "view_attendance.py",
    "send_email": "send_it_to_email.py",
    "clear": "clear.py"
}

def run_script(script_path):
    try:
        print(f"\n▶️ Running: {script_path}")
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {script_path}: {e}")

def unified_process():
    print("📦 Starting Unified Attendance System\n" + "="*40)

    # Step 1: Register Student
    run_script(scripts["registration"])

    # Step 2: Train Model
    run_script(scripts["training"])

    # Step 3: Mark Attendance
    run_script(scripts["attendance"])

    # Step 4: View Attendance (optional display)
    run_script(scripts["view"])

    # Step 5: Send Attendance via Email
    run_script(scripts["send_email"])

    # Step 6: Optional Clean-up
    cleanup_choice = input("\n🧹 Do you want to clean up .csv/.xlsx/images? (yes/no): ").strip().lower()
    if cleanup_choice == "yes":
        run_script(scripts["clear"])

    print("\n✅ All steps completed!")

if __name__ == "__main__":
    unified_process()

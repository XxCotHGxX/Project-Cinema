import subprocess
import os
from . import config

def mount_storage():
    # Construct the network path
    remote_path = f"\\\\{config.STORAGE_HOST}\\{config.STORAGE_SHARE}"
    
    # Check if already mounted
    if os.path.exists(f"{config.DRIVE_LETTER}:"):
        print(f"Drive {config.DRIVE_LETTER}: already exists.")
        return True

    print(f"Mounting {remote_path} to {config.DRIVE_LETTER}:...")
    
    cmd = [
        "net", "use", f"{config.DRIVE_LETTER}:", 
        remote_path, 
        f"/user:{config.STORAGE_USER}", 
        config.STORAGE_PASS, 
        "/persistent:yes"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("Mount successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Mount failed: {e.stderr.decode()}")
        return False

def unmount_storage():
    cmd = ["net", "use", f"{config.DRIVE_LETTER}:", "/delete", "/yes"]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("Unmount successful.")
    except:
        print("Unmount failed or drive not found.")

if __name__ == "__main__":
    mount_storage()

import os
import shutil
import glob

# Paths
DOWNLOADS = r"C:\Users\herna\Downloads"
PROJECT_VIDEOS = r"D:\ProgD\ProjectCinema\videos"
EXTENSIONS = ['*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv']

def import_downloads():
    if not os.path.exists(DOWNLOADS):
        print(f"Downloads folder not found at {DOWNLOADS}")
        return

    count = 0
    for ext in EXTENSIONS:
        files = glob.glob(os.path.join(DOWNLOADS, "**", ext), recursive=True)
        for f in files:
            dest = os.path.join(PROJECT_VIDEOS, os.path.basename(f))
            print(f"Importing: {f} -> {dest}")
            shutil.copy2(f, dest)
            count += 1
    
    print(f"Imported {count} videos.")

if __name__ == "__main__":
    import_downloads()

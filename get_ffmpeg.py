import os
import requests
import zipfile
import io

def download_ffmpeg():
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    target_dir = os.path.join(os.getcwd(), "bin")
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"Downloading FFmpeg from {url}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # Find the ffmpeg.exe inside the zip
            for file in zip_ref.namelist():
                if file.endswith("ffmpeg.exe"):
                    filename = os.path.basename(file)
                    with zip_ref.open(file) as source, open(os.path.join(target_dir, filename), "wb") as target:
                        target.write(source.read())
                    print(f"Extracted {filename} to {target_dir}")
                    return True
    else:
        print(f"Failed to download FFmpeg. Status: {response.status_code}")
        return False

if __name__ == "__main__":
    download_ffmpeg()

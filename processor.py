import subprocess
import os
import json

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "bin", "ffmpeg.exe")

def generate_thumbnail(video_path, output_path, timestamp="00:00:05"):
    """
    Generates a thumbnail for a video at a specific timestamp.
    """
    if not os.path.exists(FFMPEG_PATH):
        print("FFmpeg not found.")
        return False

    cmd = [
        FFMPEG_PATH,
        "-ss", timestamp,
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        output_path,
        "-y"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating thumbnail: {e.stderr.decode()}")
        return False

def get_video_info(video_path):
    """
    Uses ffprobe (if available) or just basic os info.
    """
    # For now, let's just stick to what we have in library.json
    pass

if __name__ == "__main__":
    # Test with a dummy video if one exists, or just verify paths
    print(f"FFmpeg path: {FFMPEG_PATH}")
    if os.path.exists(FFMPEG_PATH):
        print("FFmpeg is ready for action.")

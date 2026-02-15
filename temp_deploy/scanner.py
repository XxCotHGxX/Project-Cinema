import os
import json
import re
from pathlib import Path
from backend.metadata import get_movie_metadata
from dotenv import load_dotenv

# Load env for standalone run
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv'}

def parse_filename(filename):
    name = Path(filename).stem
    clean_name = re.sub(r'[\._]', ' ', name)
    year_match = re.search(r'\b(19|20)\d{2}\b', clean_name)
    year = year_match.group(0) if year_match else None
    if year:
        title = clean_name.split(year)[0].strip()
    else:
        title = re.sub(r'\b(1080p|720p|2160p|4k|bluray|h264|x264|h265|x265|web-dl)\b.*', '', clean_name, flags=re.I).strip()
    return title, year

def scan_videos(directory):
    video_list = []
    path = Path(directory)
    if not path.exists():
        print(f"Path {directory} not found.")
        return []

    for file in path.rglob('*'):
        if file.suffix.lower() in VIDEO_EXTENSIONS:
            title, year = parse_filename(file.name)
            print(f"Enriching: {title} ({year if year else 'N/A'})...")
            
            # Pull from TMDB
            meta = get_movie_metadata(title, year)
            
            item = {
                "title": title,
                "year": year,
                "filename": file.name,
                "path": str(file.absolute()),
                "size_mb": round(file.stat().st_size / (1024 * 1024), 2),
                "extension": file.suffix,
                "description": meta["description"] if meta else "No synopsis available.",
                "poster_url": meta["poster_url"] if meta else "https://via.placeholder.com/500x750?text=No+Poster",
                "backdrop_url": meta["backdrop_url"] if meta else ""
            }
            video_list.append(item)
    
    return video_list

if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(__file__), "videos")
    results = scan_videos(target_dir)
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "library.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Scan complete. Found {len(results)} videos with metadata. Library saved to {output_path}")

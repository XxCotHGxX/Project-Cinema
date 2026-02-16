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
    
    # Detect TV show patterns (S01E01, 1x01, etc.)
    tv_match = re.search(r'S(\d+)E(\d+)', clean_name, re.I)
    if not tv_match:
        tv_match = re.search(r'(\d+)x(\d+)', clean_name, re.I)
    
    if tv_match:
        season = int(tv_match.group(1))
        episode = int(tv_match.group(2))
        title = clean_name[:tv_match.start()].strip()
        return title, None, "TV", season, episode

    year_match = re.search(r'\b(19|20)\d{2}\b', clean_name)
    year = year_match.group(0) if year_match else None
    if year:
        title = clean_name.split(year)[0].strip()
    else:
        title = re.sub(r'\b(1080p|720p|2160p|4k|bluray|h264|x264|h265|x265|web-dl)\b.*', '', clean_name, flags=re.I).strip()
    return title, year, "Movie", None, None

def scan_videos(directory):
    video_list = []
    path = Path(directory)
    if not path.exists():
        print(f"Path {directory} not found.")
        return []

    print(f"Scanning directory: {path.absolute()}")
    for file in path.rglob('*'):
        if file.is_dir():
            # print(f"Checking subfolder: {file.relative_to(path)}")
            continue
            
        if file.suffix.lower() in VIDEO_EXTENSIONS:
            title, year, media_type, season, episode = parse_filename(file.name)
            
            # Detect genre/category from subfolder name
            relative_path = file.relative_to(path)
            genre = relative_path.parts[0] if len(relative_path.parts) > 1 else "Uncategorized"
            
            # If subfolder name is "Movies" or "TV Shows", use that to override media_type
            if "movie" in genre.lower():
                media_type = "Movie"
            elif "tv" in genre.lower() or "show" in genre.lower():
                media_type = "TV"

            print(f"Found: {relative_path} [{media_type}] -> Enriching: {title}...")
            
            # Pull from TMDB
            from backend.metadata import get_tv_metadata
            if media_type == "TV":
                meta = get_tv_metadata(title)
            else:
                meta = get_movie_metadata(title, year)
            
            item = {
                "title": title,
                "year": year,
                "filename": file.name,
                "path": str(file.absolute()),
                "genre": genre,
                "media_type": media_type,
                "season": season,
                "episode": episode,
                "size_mb": round(file.stat().st_size / (1024 * 1024), 2),
                "extension": file.suffix,
                "description": meta["description"] if meta else "No synopsis available.",
                "poster_url": meta["poster_url"] if meta else "https://via.placeholder.com/500x750?text=No+Poster",
                "backdrop_url": meta["backdrop_url"] if meta else "",
                "rating": meta.get("rating", 0) if meta else 0
            }
            video_list.append(item)
    
    return video_list

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.join(os.path.dirname(__file__), "videos")
        
    results = scan_videos(target_dir)
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "library.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Scan complete. Found {len(results)} videos with metadata. Library saved to {output_path}")

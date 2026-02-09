import os
import requests
import json
from .config import settings

def get_movie_metadata(title, year=None):
    """
    Searches TMDB for movie info based on parsed title and year.
    Returns synopsis, poster_url, and backdrop_url.
    """
    if not settings.TMDB_API_KEY:
        print("TMDB_API_KEY missing in config")
        return None

    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    }
    if year:
        params["year"] = year

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json().get('results')

        if results:
            best_match = results[0]
            return {
                "description": best_match.get("overview"),
                "poster_url": f"https://image.tmdb.org/t/p/w500{best_match.get('poster_path')}",
                "backdrop_url": f"https://image.tmdb.org/t/p/original{best_match.get('backdrop_path')}",
                "rating": best_match.get("vote_average"),
                "release_date": best_match.get("release_date")
            }
    except Exception as e:
        print(f"Error fetching metadata for {title}: {e}")
    
    return None

if __name__ == "__main__":
    # Test with a known movie
    test_title = "The Matrix"
    test_year = "1999"
    print(f"Testing metadata for {test_title}...")
    info = get_movie_metadata(test_title, test_year)
    if info:
        print("Match found!")
        print(f"Title: {test_title}")
        print(f"Synopsis: {info['description'][:100]}...")
    else:
        print("No match found.")

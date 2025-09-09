import requests
from dotenv import load_dotenv
import os

load_dotenv()
# TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# if TMDB_API_KEY:
#     print("TMDB API key loaded successfully")
API_KEY = st.secrets.get("TMDB_API_KEY", os.getenv("TMDB_API_KEY"))
# Debug print
st.write("API key loaded:", bool(API_KEY))

BASE_URL = "https://api.themoviedb.org/3"

def search_movie(title):
    """Search movie by title and return details."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}
    res = requests.get(url, params=params, timeout=10, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
    res = res.json()


    if res.get("results"):
        movie = res["results"][0]  # first match
        movie_id = movie["id"]
        return get_movie_details(movie_id)
    else:
        return {"error": "Movie not found"}

def get_movie_details(movie_id):
    """Fetch movie details, poster, and trailers by ID."""
    # 1. Movie details
    details_url = f"{BASE_URL}/movie/{movie_id}"
    details = requests.get(details_url, params={"api_key": TMDB_API_KEY}).json()
    # print(details)

    # 2. Poster (full image URL)
    poster_url = None
    if details.get("poster_path"):
        poster_url = f"https://image.tmdb.org/t/p/w500{details['poster_path']}"

    # 3. Trailer (YouTube key)
    videos_url = f"{BASE_URL}/movie/{movie_id}/videos"
    videos = requests.get(videos_url, params={"api_key": TMDB_API_KEY}).json()

    trailer_url = None
    for v in videos.get("results", []):
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            trailer_url = f"https://www.youtube.com/watch?v={v['key']}"
            break

    return {
        "title": details.get("title"),
        "overview": details.get("overview"),
        "release_date": details.get("release_date"),
        "rating": details.get("vote_average"),
        "poster_url": poster_url,
        "trailer_url": trailer_url,
        "budget" : details.get("budget"),
        "revenue" : details.get("revenue"),
        "genres" : details.get("genres"),
    }


print(search_movie("Inception"))

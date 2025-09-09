import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if TMDB_API_KEY:
    print("TMDB API key loaded successfully")
    
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

def search_movie(query):
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    r = requests.get(url, params=params).json()
    if r.get("results"):
        return r["results"][0]
    return None

def get_movie_details(movie_id):
    """Fetch full details: credits, images, videos, release dates, providers."""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,images,videos,release_dates,watch/providers"
    }
    return requests.get(url, params=params).json()

def get_cast_with_images(credits, limit=10):
    cast_list = []
    for actor in credits.get("cast", [])[:limit]:
        cast_list.append({
            "name": actor["name"],
            "character": actor.get("character", ""),
            "profile": IMG_BASE + actor["profile_path"] if actor.get("profile_path") else None
        })
    return cast_list

def get_release_info(details):
    """Return certifications (ratings) by country."""
    releases = details.get("release_dates", {}).get("results", [])
    info = []
    for rel in releases:
        country = rel["iso_3166_1"]
        certs = [r.get("certification") for r in rel.get("release_dates", []) if r.get("certification")]
        if certs:
            info.append({"country": country, "certification": certs[0]})
    return info

def get_watch_providers(details):
    """Return streaming providers per region."""
    providers = details.get("watch/providers", {}).get("results", {})
    result = {}
    for region, data in providers.items():
        flatrate = [p["provider_name"] for p in data.get("flatrate", [])]
        if flatrate:
            result[region] = flatrate
    return result


def get_movie_composers(movie_name):
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    """Fetch music composers (with photos) for a movie using TMDb API."""
    # Step 1: Search movie
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_name}
    response = requests.get(search_url, params=params).json()

    if not response["results"]:
        return None, []

    movie_id = response["results"][0]["id"]
    movie_title = response["results"][0]["title"]

    # Step 2: Get credits
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    credits = requests.get(credits_url, params={"api_key": TMDB_API_KEY}).json()

    # Step 3: Filter for composers
    composers = []
    for member in credits.get("crew", []):
        if member.get("job") in ["Original Music Composer", "Music"]:
            composers.append({
                "name": member["name"],
                "profile": IMAGE_BASE_URL + member["profile_path"] if member.get("profile_path") else None
            })

    return movie_title, composers


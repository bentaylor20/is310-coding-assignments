
import json
import time
import apikey
import requests
from rich.console import Console

console = Console()
HEADERS = {"User-Agent": "bent5@illinois.edu"}
WIKI_API = "https://marvelcinematicuniverse.fandom.com/api.php"

TMDB_MOVIES = "https://api.themoviedb.org/3/discover/movie"
TMDB_HEADERS = {**HEADERS, "Authorization": "Bearer " + apikey.load("TMDB_API_TOKEN")}

def get_json(url, params, headers=HEADERS):
    """Return parsed JSON, or None if the request fails."""
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
    except requests.RequestException as err:
        console.print("Request failed: {err}")
        return None
    time.sleep(0.5)
    if response.status_code != 200:
        console.print("HTTP {response.status_code} for {url}")
        return None
    return response.json()

data = get_json(WIKI_API, {
    "action": "query", "list": "search", "srsearch": "Iron Man",
    "srlimit": "10", "format": "json",
})
members = data["query"]["search"] if data else []
console.print(members)

data = get_json(TMDB_MOVIES, {"with_companies": 420, "sort_by": "primary_release_date.asc", "primary_release_date.gte": "2008-01-01"},
                headers=TMDB_HEADERS)
movies = [{"id": m["id"], "title": m["title"], "release_date": m["release_date"]}
          for m in (data["results"][:10] if data else [])]
console.print(movies)

links = []
for movie in movies:
    data = get_json(WIKI_API, {
        "action": "query", "titles": movie["title"], "redirects": 1, "prop": "langlinks", "lllimit": "max", "format": "json",
        })
    page = next(iter(data["query"]["pages"].values())) if data else {}
    found = bool(page) and "missing" not in page
    links.append({
        "tmdb_title": movie["title"],
        "wiki_title": page.get("title") if found else None,
        "language_links": len(page.get("langlinks", [])) if found else None,
    })
console.print(links)

for name, records in [("fandom_mcu_category_members", members),
                      ("tmdb_marvel_movies", movies),
                      ("tmdb_fandom_links", links)]:
    with open("marvel_movies.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    

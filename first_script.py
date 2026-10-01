favorite_movies = [
    {"Movie": "Big Hero 6", "Year": 2014},
    {"Movie": "How To Train Your Dragon", "Year": 2010},
    {"Movie": "Goodwill Hunting", "Year": 1997},
    {"Movie": "Iron Claw", "Year": 2020},
    {"Movie": "Seven", "Year": 1995}
]

def check_movie_year(movie):
    if movie["Year"] < 2000:
        print("This movie was released before 2000")
    else:
        print("This movie was released after 2000")
        return movie["Movie"]

recent_movies = []

for movie in favorite_movies:
    result = check_movie_year(movie)
    if result is not None:
        recent_movies.append(result)

print("Recent movies:", recent_movies)
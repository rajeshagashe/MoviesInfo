from app.models.movies import MoviesData
from app.extensions import sql_db
import sys
import json

def run():
    print("Populating Database...")
    
    with open('src/imdb.json') as movies:
        movies_json = json.load(movies)

    for doc in movies_json:
        try:
            movie = MoviesData()
            
            movie.name = doc.get("name")
            movie.nn_popularity = doc.get("99popularity")
            movie.director = doc.get("director")
            movie.genre = ','.join(sorted([i.strip() for i in doc.get("genre")]))
            movie.imdb_score = doc.get("imdb_score")
            
            sql_db.session.add(movie)
            sql_db.session.commit()

        except Exception as e:
            print(e)
            continue

        

    
if __name__ == "__main__":
    run()

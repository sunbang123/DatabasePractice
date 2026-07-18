from pymongo import MongoClient

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017")
db = client["movie_db"]
collection = db["top_rated_movies"] 

target_movie = db.top_rated_movies.find_one({'title':'마이클'})
target_year = target_movie['released_year']
print(target_year)

movies = list(db.top_rated_movies.find({'released_year':target_year}))

for movie in movies:
    print(movie['title'])
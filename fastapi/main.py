from urllib import request
import json 
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# gets the rating of a movie from imdb
@app.get("/movie/imdb/{movie_name}")
async def get_movie_rating(movie_name: str):
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    # get imdbRating from the response
    return {"rating": data["imdbRating"]}
    
# get the rating of a movie from the movie database
@app.get("/movie/tmdb/{movie_name}")
async def get_movie_rating(movie_name: str):
    url = "https://api.themoviedb.org/3/search/movie?api_key=d8f8f0d8f8f0d8f8f0d8f8f0d8f8f0d&query=" + movie_name
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    # get the first movie from the response
    movie = data["results"][0]
    # get the rating from the movie
    return {"rating": movie["vote_average"]}
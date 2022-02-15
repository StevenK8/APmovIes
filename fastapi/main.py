from urllib import request
import json 
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# gets the rating of a movie from imdb
@app.get("/movie/{movie_name}")
async def get_movie_rating(movie_name: str):
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    # get imdbRating from the response
    return {"rating": data["imdbRating"]}
    
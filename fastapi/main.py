from urllib import request
import json 
from fastapi import FastAPI
from bs4 import BeautifulSoup

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
    return {"original_title" : data["Title"],"rating": float(data["imdbRating"]), "vote_count": int(data["imdbVotes"].replace(",", ""))}
    
# get the rating of a movie from the movie database
@app.get("/movie/tmdb/{movie_name}")
async def get_movie_rating(movie_name: str):
    url = "https://api.themoviedb.org/3/search/movie?api_key=aa643d7ba8d154d4da222aaf9dc63aba&query=" + movie_name
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    # get the first movie from the response
    movie = data["results"][0]
    # get the rating from the movie
    return {"original_title" : movie["original_title"], "rating": movie["vote_average"], "vote_count": movie["vote_count"]}

# gets the rating of a movie from metacritic
@app.get("/movie/metacritic/{movie_name}")
async def get_movie_rating(movie_name: str):
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    # get imdbRating from the response
    return {"original_title" : data["Title"],"rating": float(data["Metascore"])/10}

@app.get("/movie/{movie_name}")
async def get_movie_rating(movie_name: str):
    urlOmdb = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    urlTmdb = "https://api.themoviedb.org/3/search/movie?api_key=aa643d7ba8d154d4da222aaf9dc63aba&query=" + movie_name


    request_responseOmdb = request.urlopen(urlOmdb)
    dataOmdb = json.loads(request_responseOmdb.read())
    request_responseTmdb = request.urlopen(urlTmdb)
    dataTmdb = json.loads(request_responseTmdb.read())

    movie = dataTmdb["results"][0]

    return {"original_title": dataOmdb["Title"], "rating": (float(dataOmdb["imdbRating"]) + movie["vote_average"] + ( float(dataOmdb["Metascore"])/10)) / 3, "vote_count": int(dataOmdb["imdbVotes"].replace(",", "")) + movie["vote_count"] }

# gets the rating of a movie by scrapping the allocine website
@app.get("/movie/allocine/{movie_name}")
async def get_movie_rating(movie_name: str):
    url = "https://www.allocine.fr/rechercher/?q=" + movie_name
    soup = BeautifulSoup(request.urlopen(url), "html.parser")
    print(soup.find("span", {"class": "xXx meta-title-link"}))

    # num_fiche_film = BeautifulSoup(request.urlopen(url).read(), "html.parser").find("a", {"class": "meta-title-link"})["href"].split("/")[-1]
    # url = "https://www.allocine.fr/film/https://www.allocine.fr/film/fichefilm-"+num_fiche_film+"/critiques/spectateurs/"
    # soup = BeautifulSoup(request.urlopen(url).read(), "html.parser")
    # # get the public rating from the website
    # rating = soup.find("span", {"class": "note"}).text
    # title = soup.find("h1", {"class": "titlebar-link"}).text
    # return {"original_title" : title, "rating": float(rating)}
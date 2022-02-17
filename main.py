from urllib import request
import json 
import pymysql
# from bs4 import BeautifulSoup
# import requests
from fastapi import FastAPI, Path
from pydantic import BaseModel

class Comment(BaseModel):
    comment: str = ""
    rate: int = Path(..., title = "rate", gt=0, le=10)

class User(BaseModel):
    name: str = ""

import configparser
CONFIG_PATH = './config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)

MYSQL_HOST = CONFIG.get('mysql', 'host')
MYSQL_USER = CONFIG.get('mysql', 'user')
MYSQL_PASSWORD = CONFIG.get('mysql', 'password')
MYSQL_DB = CONFIG.get('mysql', 'db')
TMDB_API_KEY = CONFIG.get('tmdb', 'api_key')

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to APmovIes ! An API that gives informations from multiple movie websites. Try /docs to access our documentation"}


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
    url = "https://api.themoviedb.org/3/search/movie?api_key="+TMDB_API_KEY+"&query=" + movie_name
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
    urlTmdb = "https://api.themoviedb.org/3/search/movie?api_key="+TMDB_API_KEY+"&query=" + movie_name


    request_responseOmdb = request.urlopen(urlOmdb)
    dataOmdb = json.loads(request_responseOmdb.read())
    request_responseTmdb = request.urlopen(urlTmdb)
    dataTmdb = json.loads(request_responseTmdb.read())

    movie = dataTmdb["results"][0]

    return {"original_title": dataOmdb["Title"], "rating": (float(dataOmdb["imdbRating"]) + movie["vote_average"] + ( float(dataOmdb["Metascore"])/10)) / 3, "vote_count": int(dataOmdb["imdbVotes"].replace(",", "")) + movie["vote_count"] }


def connect_db():
    return pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)

@app.post("/movie/{movie_name}/")
async def post_comment(movie_name : str, comment : Comment):
    #todo --> put bd
    return comment 

@app.get("/movie/{movie_name}/comments")
async def get_comments(movie_name: str):
    #todo --> appel à la bd
    return 

@app.post("/{name}")
async def create_user(user: User):
    #todo --> call db
    return user;

@app.delete("/{name}")
async def delete_user(name: str):
    #todo --> call db
    return 

# @app.get("/mycomments/{name}")
# def get_albums(name: str):
#     db = connect_db()
#     cur = db.cursor()
#     cur.execute("SELECT ")
#     mesures = cur.fetchall() 
#     cur.close()
#     del cur
#     db.close()
#     return mesures


# gets the rating of a movie by scrapping the allocine website
# @app.get("/movie/allocine/{movie_name}")
# async def get_movie_rating(movie_name: str):
#     url = "https://www.allocine.fr/rechercher/?q=" + movie_name
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, "html.parser")
#     print(soup.find("h2").findChildren())
    # num_fiche_film = BeautifulSoup(request.urlopen(url).read(), "html.parser").find("a", {"class": "meta-title-link"})["href"].split("/")[-1]
    # url = "https://www.allocine.fr/film/https://www.allocine.fr/film/fichefilm-"+num_fiche_film+"/critiques/spectateurs/"
    # soup = BeautifulSoup(request.urlopen(url).read(), "html.parser")
    # # get the public rating from the website
    # rating = soup.find("span", {"class": "note"}).text
    # title = soup.find("h1", {"class": "titlebar-link"}).text
    # return {"original_title" : title, "rating": float(rating)}
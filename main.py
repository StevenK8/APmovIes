from cmath import log
from urllib import request, response
import json 
import pymysql
# from bs4 import BeautifulSoup
# import requests
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, JsonError, UrlError

from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey


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
async def get_movie_rating_imdb(movie_name: str):
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    
    if(data["Response"] == "True"):
        # get imdbRating from the response
        return {"original_title" : data["Title"],"rating": float(data["imdbRating"]), "vote_count": int(data["imdbVotes"].replace(",", ""))}
    else:
        return {"Error": "Movie not found"}
    
# get the rating of a movie from the movie database
@app.get("/movie/tmdb/{movie_name}")
async def get_movie_rating_tmdb(movie_name: str):
    url = "https://api.themoviedb.org/3/search/movie?api_key="+TMDB_API_KEY+"&query=" + movie_name
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    
    if(data["total_results"] != 0):
        # get the first movie from the response
        movie = data["results"][0]
        # get the rating from the movie
        return {"original_title" : movie["original_title"], "rating": movie["vote_average"], "vote_count": movie["vote_count"]}
    else:
        return {"Error": "Movie not found"}

# gets the rating of a movie from metacritic
@app.get("/movie/metacritic/{movie_name}")
async def get_movie_rating_metacritic(movie_name: str):
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    if(data["Response"] == "True"):
        # get imdbRating from the response
        return {"original_title" : data["Title"],"rating": float(data["Metascore"])/10}
    else:
        return {"Error": "Movie not found"}

@app.get("/movie/{movie_name}")
async def get_movie_rating_api(movie_name: str):
    imdb = await get_movie_rating_imdb(movie_name)
    tmdb = await get_movie_rating_tmdb(movie_name)
    metacritic = await get_movie_rating_metacritic(movie_name)
    try :
        if(imdb["Error"] == "Movie not found"):
            return imdb
        elif tmdb["Error"] == "Movie not found":
            return tmdb
        elif metacritic["Error"] == "Movie not found":
            return metacritic
    except:
        return {"original_title": imdb["original_title"], "rating": (float(imdb["rating"]) + tmdb["rating"] + float(metacritic["rating"])) / 3, "vote_count": int(imdb["vote_count"]) + tmdb["vote_count"]}


def connect_db():
    return pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)


@app.post("/movie")
async def post_comment(apikey: str, movieName : str, comment : str, rate : int):
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT id from users where apikey=%s", (apikey))
        idu = cur.fetchall();
        if cur.rowcount == 0:
            return {
            "error" : "wrong apikey !"
            }
        else:
            cur.execute("SELECT id from movies where title=%s", (movieName))
            idm = cur.fetchall()
            if cur.rowcount == 0:
                return {
                    "error" : "this movie doesn't exist or is not in DB"
                }
            else:
                cur.execute("INSERT INTO comments(idu, idm, rating, text) VALUES (%s,%s,%s,%s)", (idu, idm, rate, comment))
                commit = db.commit()
                cur.close()
                del cur
                db.close()
    except HTTPException as e:
        log.debug(e)
    return {"comment" : comment, "rate" : rate}

@app.get("/movie/{movie_name}/comments")
async def get_comments(movie_name: str):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT text, rating FROM comments c, movies m WHERE c.idm = m.id and m.title=%s", (movie_name))
    comments = cur.fetchall() 
    if cur.rowcount == 0:
        return {
        "error" : "wrong movie name !"
        }
    cur.close()
    del cur
    db.close()
    return comments

@app.post("/")
async def create_user(name: str):
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users(name) VALUES (%s)", (name))
        user = db.commit()

        cur.execute("SELECT apikey from users where name=%s", (name))
        apiKeyUser = cur.fetchall()

        db.close()
    except HTTPException as e:
        log.debug(e)
    return "Your apikey : " , apiKeyUser, " keep it confidential"

@app.delete("/")
async def delete_user(apikey: str):
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("DELETE FROM users WHERE apikey=%s", (apikey))
        user = db.commit()
        db.close()
    except HTTPException as e:
        log.debug(e)
    return user
     

@app.get("/mycomments/{name}")
def get_mycomments(apikey: str):
    db = connect_db()
    cur = db.cursor()

    cur.execute("SELECT id from users where apikey=%s", (apikey))
    idu = cur.fetchall()
    if cur.rowcount == 0:
        return {
        "error" : "wrong apikey !"
        }
    else:
        cur.execute("SELECT rating, text FROM comments WHERE idu=%s", (idu))
        mycomments = cur.fetchall() 
        cur.close()
        del cur
        db.close()
        return mycomments


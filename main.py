from cmath import log
from urllib import request, response
import json
import pymysql
import asyncio

# from bs4 import BeautifulSoup
# import requests
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, JsonError, UrlError
from typing import Optional


import configparser
CONFIG_PATH = './config/config.ini'
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
    return {"message": "Welcome to APmovIes ! An API that gives information from multiple movie websites. Try /docs to access our documentation"}


# gets the rating of a movie from imdb
@app.get("/movie/imdb/{movie_name}")
def get_movie_rating_imdb(movie_name: str):
    movie_name = parse_title(movie_name)
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())

    if(data["Response"] == "True" and data["imdbRating"] != "N/A"):
        # get imdbRating from the response
        return {"original_title": data["Title"], "rating": float(data["imdbRating"]), "vote_count": int(data["imdbVotes"].replace(",", "")), "id": data["imdbID"]}
    else:
        return {"Error": "Movie not found"}

# get the rating of a movie from the movie database
@app.get("/movie/tmdb/{movie_name}")
def get_movie_rating_tmdb(movie_name: str):
    movie_name = parse_title_tmdb(movie_name)
    url = "https://api.themoviedb.org/3/search/movie?api_key=" + \
        TMDB_API_KEY+"&query=" + movie_name
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())

    if(data["total_results"] != 0):
        # get the first movie from the response
        movie = data["results"][0]
        # get the rating from the movie
        return {"original_title": movie["original_title"], "rating": movie["vote_average"], "vote_count": movie["vote_count"]}
    else:
        return {"Error": "Movie not found"}

# gets the rating of a movie from metacritic
@app.get("/movie/metacritic/{movie_name}")
def get_movie_rating_metacritic(movie_name: str):
    movie_name = parse_title(movie_name)
    url = "http://www.omdbapi.com/?t=" + movie_name + "&apikey=thewdb"
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())
    if(data["Response"] == "True" and data["Metascore"] != "N/A"):
        # get imdbRating from the response
        return {"original_title": data["Title"], "rating": float(data["Metascore"])/10}
    else:
        return {"Error": "Movie not found"}


@app.get("/movie/rating/")
def get_movie_rating_api(movie_name: str):
    imdb = get_movie_rating_imdb(movie_name)
    tmdb = get_movie_rating_tmdb(movie_name)
    metacritic = get_movie_rating_metacritic(movie_name)

    if("Error" in imdb or "Error" in tmdb or "Error" in metacritic):
        return {"Error": "Movie not found"}
    else:
        return {"original_title": imdb["original_title"], "rating": (float(imdb["rating"]) + tmdb["rating"] + float(metacritic["rating"])) / 3, "vote_count": int(imdb["vote_count"]) + tmdb["vote_count"]}


@app.get("/movie/top_rated")
def get_top_rating(page: int = 1):
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key=" + \
        TMDB_API_KEY+"&language=en-US&region=fr&page=" + str(page)
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())

    return data


def connect_db():
    return pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)


def parse_title(title):
    # Capitalize the first letter of each word
    # title = title.title()
    title = ' '.join([w.title() if w.islower() else w for w in title.split()])
    # Replace spaces or underscores or dashes with '+'
    title = title.replace("+", "_")
    title = title.replace("-", "_")
    return title.replace(" ", "_")


def parse_title_tmdb(title):
    # title = title.title()
    title = ' '.join([w.title() if w.islower() else w for w in title.split()])
    # Replace spaces or underscores or dashes with '+'
    title = title.replace("+", "")
    title = title.replace("-", "")
    return title.replace(" ", "")


@app.post("/movie/{movie_name}/comment")
async def post_comment(
        apikey: str,
        movie_name: str,
        rate: float = Query(..., ge=0, le=10),
        comment: Optional[str] = Query(None, max_length=150)):

    movie_name = parse_title(movie_name)
    if (rate > 10 or rate < 0):
        return {"Error": "Rate must be between 0 and 10"}
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT id from users where apikey=%s", (apikey))
        idu = cur.fetchone()[0]
        if cur.rowcount == 0:
            return {
                "error": "wrong apikey !"
            }
        else:
            # Authenticated
            idm = createMovieIfNotExist(movie_name)
            if (idm == ""):
                return {
                    "error": "movie not found"
                }

            cur.execute(
                "SELECT c.id from comments c, users u, movies m where c.idu=u.id AND m.id=c.idm AND apikey=%s AND m.title like %s", (apikey, movie_name))

            if cur.rowcount < 1:
                cur.execute(
                    "INSERT INTO comments(idu, idm, rating, text) VALUES (%s,%s,%s,%s)", (idu, idm, rate, comment))
                db.commit()
            else:
                cur.execute(
                    "UPDATE comments SET rating = %s, text = %s WHERE comments.idm = %s AND comments.idu = %s;", (rate, comment, idm, idu))
                db.commit()

        cur.close()
        del cur
        db.close()
    except HTTPException as e:
        log.debug(e)
    return {"title": movie_name,"comment": comment, "rate": rate}


def createMovieIfNotExist(title):
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT id from movies where title=%s", (title))
        if cur.rowcount == 0:
            imdb = get_movie_rating_imdb(title)
            try:
                idm = imdb["id"]
                cur.execute(
                    "INSERT INTO movies(id, title) VALUES (%s,%s)", (idm, title))
                db.commit()
            except:
                idm = ""
            print(title)
        else:
            idm = cur.fetchone()[0]
            
        return idm
    except HTTPException as e:
        log.debug(e)


@app.get("/movie/{movie_name}/comments")
async def get_comments(movie_name: str):
    movie_name = parse_title(movie_name)
    db = connect_db()
    cur = db.cursor()
    cur.execute(
        "SELECT name, text, rating FROM comments c, movies m, users u WHERE c.idm = m.id and u.id=c.idu and m.title=%s", (movie_name))
    comments = cur.fetchall()
    if cur.rowcount == 0:
        return {
            "error": "wrong movie name !"
        }
    cur.close()
    del cur
    db.close()
    return comments

@app.get("/movie/{movie_name}/")
async def get_rating_apmovie(movie_name: str):
    movie_name = parse_title(movie_name)
    db = connect_db()
    cur = db.cursor()
    cur.execute(
        "SELECT avg(rating) FROM comments c, movies m WHERE c.idm = m.id and m.title=%s", (movie_name))
    avgRating = cur.fetchall()
    if cur.rowcount == 0:
        return {
            "error": "wrong movie name !"
        }
    cur.close()
    del cur
    db.close()
    return avgRating;


@app.post("/")
async def create_user(name: str):
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users(name) VALUES (%s)", (name))
        db.commit()

        cur.execute("SELECT apikey from users where name=%s", (name))
        apiKeyUser = cur.fetchall()

        db.close()
    except HTTPException as e:
        log.debug(e)
    return "Your apikey : ", apiKeyUser, " keep it confidential"


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

@app.delete("/mycomment")
async def delete_comment(apikey: str, movie_name: str):
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE apikey=%s", (apikey))
        idu = cur.fetchall()

        if cur.rowcount == 0:
            return {
                "error": "wrong apikey !"
            }
        else:
            cur.execute("SELECT id FROM movies WHERE title=%s", (movie_name))
            idm = cur.fetchone()[0]
            if cur.rowcount == 0:
                return {
                    "error": "wrong title !"
                }
            else:
                cur.execute("DELETE FROM comments WHERE idu=%s AND idm=%s", (idu, idm))
                cur.close()
                del cur
                db.commit()
                db.close()
                return mycomment
    except HTTPException as e:
        log.debug(e)
    return mycomment

@app.get("/mycomments/")
def get_mycomments(apikey: str):
    db = connect_db()
    cur = db.cursor()

    cur.execute("SELECT id from users where apikey=%s", (apikey))
    idu = cur.fetchall()
    if cur.rowcount == 0:
        return {
            "error": "wrong apikey !"
        }
    else:
        cur.execute("SELECT m.title, c.rating, c.text FROM comments c, movies m WHERE m.id=c.idm AND idu=%s", (idu))
        mycomments = cur.fetchall()
        cur.close()
        del cur
        db.close()
        return mycomments

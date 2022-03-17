from cmath import log
from datetime import date
import datetime
from urllib import request, response
import json
import pymysql
import asyncio

# from bs4 import BeautifulSoup
# import requests
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, JsonError, UrlError, Field
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

    if "Error" in imdb :
        if "Error" in tmdb:
            if "Error" in metacritic:
                return {"Error": "Movie not found"}
            else: 
                return {"original_title": metacritic["original_title"], "rating": float(metacritic["rating"])}
        else:
            if "Error" in metacritic:
                return {"original_title": tmdb["original_title"], "rating": tmdb["rating"], "vote_count": tmdb["vote_count"]}
            else:
                return {"original_title": metacritic["original_title"], "rating": (tmdb["rating"] + float(metacritic["rating"])) / 2, "vote_count": tmdb["vote_count"]}
    else:
        if "Error" in tmdb:
            if "Error" in metacritic:
               return {"original_title": imdb["original_title"], "rating": float(imdb["rating"]), "vote_count": int(imdb["vote_count"])}
            else:
                return {"original_title": imdb["original_title"], "rating": (float(imdb["rating"]) + float(metacritic["rating"])) / 2, "vote_count": int(imdb["vote_count"]) }
        else:
            if "Error" in metacritic:
                return {"original_title": imdb["original_title"], "rating": (float(imdb["rating"]) + tmdb["rating"]) / 2, "vote_count": int(imdb["vote_count"]) + tmdb["vote_count"]}
            else:
                return {"original_title": imdb["original_title"], "rating": (float(imdb["rating"]) + tmdb["rating"] + float(metacritic["rating"])) / 3, "vote_count": int(imdb["vote_count"]) + tmdb["vote_count"]}

@app.get("/movie/top_rated")
def get_top_rating(page: int = 1, date_min: Optional[date] = None, date_max: Optional[date] = None):
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key=" + \
        TMDB_API_KEY+"&language=en-US&region=fr&page=" + str(page)
    # Get json data from the url
    request_response = request.urlopen(url)
    data = json.loads(request_response.read())

    filtered_data = []
    print(date_min)
    
    # Filter data by date
    for movie in data["results"]:
        if(date_min is not None and date_max is not None):
            if(later_than(movie["release_date"] , date_min) and not later_than(movie["release_date"] , date_max)):
                # data["results"].remove(movie)
                filtered_data.append(movie)
        elif(date_min is not None):
            if(later_than(movie["release_date"] , date_min)):
                # data["results"].remove(movie)
                filtered_data.append(movie)
        elif(date_max is not None):
            if(not later_than(movie["release_date"] , date_max)):
                # data["results"].remove(movie)
                filtered_data.append(movie)
        else:
            filtered_data.append(movie)

    return filtered_data

# Compares two dates
def later_than(date1, date2):
    # convert date1 to date object
    date1 = date1.split("-")
    date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
    if(date1 > date2):
        return True
    else:
        return False

# Compares dates that are in the format YYYY-MM-DD
# def later_than(date1, date2):
#     date1 = date1.split("-")
#     date2 = date2.split("-")
#     if(len(date1)>=1 and len(date2)>=1):
#         if(int(date1[0]) > int(date2[0])):
#             return True
#         elif(int(date1[0]) < int(date2[0])):
#             return False
#         if (len(date1)>=2 and len(date2)>=2):
#             if(int(date1[1]) > int(date2[1])):
#                 return True
#             elif(int(date1[1]) < int(date2[1])):
#                 return False
#             if (len(date1)>=3 and len(date2)>=3):
#                 if(int(date1[2]) > int(date2[2])):
#                     return True
#                 elif(int(date1[2]) < int(date2[2])):
#                     return False
#                 else:
#                     return False
#             else:
#                 return False
#     return False

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
        "SELECT title, name, text, rating FROM comments c, movies m, users u WHERE c.idm = m.id and u.id=c.idu and m.title=%s", (movie_name))
    comments = cur.fetchall()
    if cur.rowcount == 0:
        return {
            "error": "wrong movie name !"
        }
    cur.close()
    del cur
    db.close()
    # return {"title": comments[0][0] ,"user": comments[0][1], "comment": comments[0][2], "rate": comments[0][3]} 
    return comments

@app.get("/movie/{movie_name}/")
async def get_rating_apmovie(movie_name: str):
    movie_name = parse_title(movie_name)
    db = connect_db()
    cur = db.cursor()
    cur.execute(
        "SELECT title, avg(rating) FROM comments c, movies m WHERE c.idm = m.id and m.title=%s", (movie_name))
    avgRating = cur.fetchall()
    if cur.rowcount == 0:
        return {
            "error": "wrong movie name !"
        }
    cur.close()
    del cur
    db.close()
    return {"title": avgRating[0][0], "rate": avgRating[0][1]} 


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
    return {"apikey": apiKeyUser[0][0]}


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
        cur.execute("SELECT u.name, m.title, c.rating, c.text FROM comments c, movies m, users u WHERE m.id=c.idm AND c.idu=u.id AND idu=%s", (idu))
        mycomments = cur.fetchall()
        cur.close()
        del cur
        db.close()
        # return {"user": mycomments[0][0], "comments" : {"title": mycomments[0][1], "rating": mycomments[0][2], "comment": mycomments[0][3]}}
        
        return mycomments

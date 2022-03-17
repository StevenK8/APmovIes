from datetime import date
from http.client import HTTPException
import main
import asyncio

import configparser
CONFIG_PATH = './config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)

async def test_create_user():
    user = await main.create_user("user_test")
    return user['apikey']
    

async def test_movie_rating():
    avatar = main.get_movie_rating_api("Avatar")
    assert 0 <= avatar["rating"] <= float('inf')
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_imdb():
    avatar = main.get_movie_rating_imdb("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_tmdb():
    avatar = main.get_movie_rating_tmdb("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert 0 <= avatar["vote_count"] <= float('inf')
    assert isinstance(avatar["original_title"], str)

async def test_movie_rating_metacritic():
    avatar = main.get_movie_rating_metacritic("Avatar")
    assert 0 <= avatar["rating"] <= 10
    assert isinstance(avatar["original_title"], str)

async def test_post_get_comment(apikey):
    postResult = await main.post_comment(apikey, "Nemo", 10, "commentaire")
    assert isinstance(postResult["comment"],str)
    assert 0 <= postResult["rate"] <= float(10) 
    comments = main.get_mycomments(apikey)
    assert comments[0][3] == "commentaire"
    assert comments[0][2] == 10
    nb_comments = len(comments)
    await main.delete_comment(apikey, "Nemo")
    comments = main.get_mycomments(apikey)
    assert len(comments) == nb_comments - 1


async def test_get_comments_movie():
    comments = await main.get_comments("Avatar")
    assert isinstance(comments[0][2],str)
    assert 0 <= float(comments[0][3]) <= 10

async def test_delete_user(apikey):
    await main.delete_user(apikey)
    try:
        comments = main.get_mycomments(apikey)
        print("ok")
    except HTTPException as e:
        print("ok : ", e)

apikey = asyncio.run(test_create_user())
asyncio.run(test_movie_rating())
asyncio.run(test_movie_rating_imdb())
asyncio.run(test_movie_rating_tmdb())
asyncio.run(test_movie_rating_metacritic())
asyncio.run(test_post_get_comment(apikey))
asyncio.run(test_get_comments_movie())
asyncio.run(test_delete_user(apikey))



